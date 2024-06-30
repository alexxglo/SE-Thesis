package com.project.config;

import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.listener.ConnectListener;
import com.corundumstudio.socketio.listener.DataListener;
import com.corundumstudio.socketio.listener.DisconnectListener;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.project.models.dtos.AttackAction;
import com.project.models.dtos.CharacterPayload;
import com.project.models.dtos.NextCharacter;
import com.project.models.wrappers.CharacterSheetsWrapper;
import com.project.models.dtos.WebclientConnection;
import com.project.models.messages.MainGameStartMessage;
import com.project.models.messages.Message;
import com.project.models.messages.StartGameMessage;
import com.project.services.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.CacheManager;
import org.springframework.stereotype.Component;

import java.util.Objects;


@Slf4j
@Component
public class SocketModule {
    private final SocketIOServer server;
    @Autowired
    private SocketService socketService;
    @Autowired
    private CacheManager cacheManager;
    @Autowired
    private GameService gameService;
    @Autowired
    private RoomService roomService;
    @Autowired
    private PlayerService playerService;
    @Autowired
    private InputService inputService;

    public SocketModule(SocketIOServer inputServer) {
        server = inputServer;
        server.addConnectListener(onConnected());
        server.addDisconnectListener(onDisconnected());
        server.addEventListener("send_message", Message.class, onChatReceived());
        server.addEventListener("intro", StartGameMessage.class, onStartGame());
        server.addEventListener("init_game", MainGameStartMessage.class, onMainGameConnect());
        server.addEventListener("emit_ch_info", String.class, onCharactersSheetReceived());
        server.addEventListener("next_action", AttackAction.class, onNextActionReceived());
        server.addEventListener("emit_next_action", String.class, onSendNextAction());
        server.addEventListener("empty_room", String.class, onEmptyRoom());

    }

    public void sendP1Input(String roomCode) { // send details to game client
        log.info("Sending P1 input to game");
        socketService.sendP1Input(roomCode);
    }

    public void lockRoom(String roomCode) { // lock room on the game client
        log.info("Locking game...");
        socketService.lockRoom(roomCode);
    }

    private DataListener<Message> onChatReceived() {
        return (senderClient, data, ackSender) -> {
            log.info(data.toString());
            Thread.sleep(5000);
            socketService.sendMessage("get_message", senderClient, data.getMessage());
        };
    }

    private ConnectListener onConnected() {
        return (client) -> {
            String room = client.getHandshakeData().getUrlParams().get("room").get(0);
            String name = room.substring(5);
            room = room.substring(0, 5);
            client.joinRoom(room);

            log.info("Socket ID[{}]  Connected to socket; Name: {}, Room: {}", client.getSessionId().toString(), name, room);
            WebclientConnection webclient = WebclientConnection.builder().name(name).code(room).cliendId(client.getSessionId()).build();
            gameService.cacheWebclientConnection(webclient);
        };

    }

    private DataListener<String> onEmptyRoom() {
        return (senderClient, data, ackSender) -> {
            roomService.emptyRoom(data);
            playerService.emptyRoom(data);
            inputService.empty(data);
            socketService.signalGameOverToClients(senderClient);
        };
    }

    private DataListener<StartGameMessage> onStartGame() {
        return (senderClient, data, ackSender) -> {
            log.info("Starting game");
//            server.getBroadcastOperations().sendEvent("start_game");
            socketService.startGame("intro_response", senderClient, data.getRoom());
        };
    }

    private DataListener<MainGameStartMessage> onMainGameConnect() {
        return (senderClient, data, ackSender) -> {
            log.info("Receiving py game connection");

            log.info("Room code: {}", data.getRoomCode());
            socketService.cacheGameClient(senderClient, data.getRoomCode());
//            socketService.sendRoomToGameClient(senderClient);
        };
    }

    private DataListener<String> onCharactersSheetReceived() {
        // receive character sheets from game client. send character sheets to web clients.
        return (senderClient, data, ackSender) -> {
            log.info("Receiving py character sheets");
            ObjectMapper mapper = new ObjectMapper();

            CharacterSheetsWrapper characterSheetsWrapper = mapper.readValue(data, CharacterSheetsWrapper.class);

            for (CharacterPayload sheet : characterSheetsWrapper.getCharacter_sheets()) {
                // for every player, get their respective webclient and send the character sheets
                String cacheKey = sheet.getName() + sheet.getRoomCode();

                WebclientConnection details = Objects.requireNonNull(cacheManager.getCache("webclient")).get(cacheKey, WebclientConnection.class);

                socketService.sendMessageToGivenClient("get_character_sheet", senderClient, details.getCliendId(), sheet);
            }
        };
    }

    private DataListener<AttackAction> onNextActionReceived() {
        // receive from web client the attack from player
        return (senderClient, data, ackSender) -> {

            SocketIOClient gameClient = Objects.requireNonNull(cacheManager.getCache("clientGameMap")).get(data.getRoom(), SocketIOClient.class);

            if (gameClient!= null) {
                gameClient.sendEvent("get_attack", data);
            }
        };
    }

    private DataListener<String> onSendNextAction() {
        // receive from game client the next player to attack
        return (senderClient, data, ackSender) -> {
            log.info("Receiving the next player to attack");
            ObjectMapper mapper = new ObjectMapper();
            NextCharacter nextCharacter = mapper.readValue(data, NextCharacter.class);

            String cacheKey = nextCharacter.getName()+nextCharacter.getRoom();
            WebclientConnection details = Objects.requireNonNull(cacheManager.getCache("webclient")).get(cacheKey, WebclientConnection.class);

            socketService.sendMessageToGivenClient("attack", senderClient, details.getCliendId(), null);
        };
    }

    private DisconnectListener onDisconnected() {
        return client -> {
            log.info("Client[{}] - Disconnected from socket", client.getSessionId().toString());
        };
    }
}
