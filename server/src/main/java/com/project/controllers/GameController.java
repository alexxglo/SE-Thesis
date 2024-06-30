package com.project.controllers;

import com.project.config.SocketModule;
import com.project.models.InputPhaseOne;
import com.project.models.Props;
import com.project.models.Room;
import com.project.models.RoomDetails;
import com.project.models.RoomResponseObject;
import com.project.models.dtos.CharacterSheet;
import com.project.services.GameService;
import com.project.services.InputService;
import com.project.services.PropsService;
import com.project.services.RoomService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.messaging.handler.annotation.DestinationVariable;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@RestController
@RequestMapping("/")
@CrossOrigin(origins = "*")
public class GameController {

    @Autowired
    RoomService roomService;
    @Autowired
    PropsService propsService;
    @Autowired
    InputService inputService;
    @Autowired
    GameService gameService;
    @Autowired
    SocketModule socketModule;

    private final String ERROR_MSG = "ERROR";
    private final String ERROR_GAME_STARTED = "GAME_STARTED";

    @GetMapping("")
    public String homepage() {
        return "Hello Stranger";
    }

    @PostMapping("/access")
    public ResponseEntity<RoomResponseObject> accessRoom(@RequestBody RoomDetails roomDetails) {
        RoomResponseObject roomResponseObject = roomService.accessRoom(roomDetails);
        if (roomResponseObject.getCode().equalsIgnoreCase(ERROR_MSG)) {
            return new ResponseEntity<>(null, HttpStatus.LOCKED);
        }
        else if (roomResponseObject.getCode().equalsIgnoreCase(ERROR_GAME_STARTED)) {
            return new ResponseEntity<>(null, HttpStatus.CONFLICT);
        }
        return new ResponseEntity<>(roomResponseObject, HttpStatus.OK);
    }

    @PostMapping("/players")
    public Room postRoom(@RequestParam String roomCode) {
        return roomService.createRoom(roomCode);
    }

    @GetMapping("/players")
    public Room getPlayers(@RequestParam String roomCode) {
        return roomService.getRoom(roomCode).orElse(null);
    }

    @PostMapping("/state")
    public ResponseEntity<Integer> getLobbySize(@RequestBody RoomDetails room) {
        int response = roomService.gameSize(room.getCode());
        if (response > 0) {
            roomService.lockRoom(room.getCode());
            socketModule.lockRoom(room.getCode());
            return new ResponseEntity<>(response, HttpStatus.OK);
        }
        return new ResponseEntity<>(0, HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/props")
    public List<Props> getProps() {
        return propsService.getProps();
    }

    @PostMapping("/phase1")
    public void addInput(@RequestBody InputPhaseOne input) {
        inputService.addToGame(input);
    }

    @PostMapping("/chsheet")
    public void addCharacterSheet(@RequestBody CharacterSheet inputSheet) {
        inputService.addCharacter(inputSheet);
        Boolean isGameReady = roomService.checkIfGameReady(inputSheet.getRoomCode()); // count fields that are now filled. If equal to number of players, fill the other spots.
        // send necessary information of the game
        if (isGameReady) {
            gameService.postP1GameData(inputSheet.getRoomCode()); // add object to cache
            socketModule.sendP1Input(inputSheet.getRoomCode());
        }
    }

    @MessageMapping("/{sessionId}")
    @SendTo("/topic/{sessionId}")
    public String test(@DestinationVariable String sessionId, @Payload String msg) throws InterruptedException {
        Thread.sleep(1000);
        System.out.println("Message received: " + msg);
        return "Subscribed with session id: " + sessionId;
    }
}
