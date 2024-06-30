package com.project.services;


import com.corundumstudio.socketio.SocketIOClient;
import com.project.models.dtos.CharacterPayload;
import com.project.models.dtos.PhaseOneDTO;
import com.project.models.messages.Message;
import com.project.models.messages.MessageType;
import com.project.models.messages.StartGameMessage;
import com.project.repositories.PlayerRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.CachePut;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
@Slf4j
public class SocketService {

    @Autowired
    PlayerRepository playerRepository;
    @Autowired
    CacheManager cacheManager;
    List<Integer> shufflePlayerNumbers = Arrays.asList(1,2,3,4);



    public void sendMessage(String eventName, SocketIOClient senderClient, String message) {
        for (
                SocketIOClient client : senderClient.getNamespace().getAllClients()) {
            if (client.getSessionId().equals(senderClient.getSessionId())) {
                client.sendEvent(eventName,
                        new Message(MessageType.SERVER, message));
            }
        }
    }

    public void sendMessageToGivenClient(String eventName, SocketIOClient senderClient, UUID clientId, CharacterPayload message) {
        SocketIOClient client = senderClient.getNamespace().getClient(clientId);
        client.sendEvent(eventName, message);
    }

    public void startGame(String eventName, SocketIOClient senderClient, String roomCode) {
        List<Integer> playerNumbers = new ArrayList<>(shufflePlayerNumbers);
        SocketIOClient gameClient = Objects.requireNonNull(cacheManager.getCache("clientGameMap")).get(roomCode, SocketIOClient.class);
        for (
                SocketIOClient client : senderClient.getNamespace().getAllClients()) {
            if (client.getSessionId() != gameClient.getSessionId()) {
                client.sendEvent(eventName, new StartGameMessage(playerNumbers.get(0)));
                log.info("Sending value {} to client id {}", playerNumbers.get(0), client.getSessionId());
                playerNumbers.remove(0);
            }
        }
    }

    public void sendP1Input(String roomCode) {
        PhaseOneDTO response =  Objects.requireNonNull(cacheManager.getCache("p1")).get(roomCode, PhaseOneDTO.class);
        SocketIOClient gameClient = Objects.requireNonNull(cacheManager.getCache("clientGameMap")).get(roomCode, SocketIOClient.class);

        if (gameClient!= null) {
            log.info("Sending response: {}", response);
            gameClient.sendEvent("get_initial_game_data", response);
        }
    }


    public void lockRoom(String roomCode) {
        SocketIOClient gameClient = Objects.requireNonNull(cacheManager.getCache("clientGameMap")).get(roomCode, SocketIOClient.class);
        if (gameClient!= null) {
            gameClient.sendEvent("lock_room");
        }
    }

    public void signalGameOverToClients(SocketIOClient senderClient) {
        for (
                SocketIOClient client : senderClient.getNamespace().getAllClients()) {
                client.sendEvent("game_over");
        }
    }

    @CachePut(value = "clientGameMap", key ="#roomCode")
    public SocketIOClient cacheGameClient(SocketIOClient senderClient, String roomCode) {
        Collections.shuffle(shufflePlayerNumbers); // shuffle array of player options
        return  senderClient;
    }
}
