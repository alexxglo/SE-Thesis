package com.project.services;

import com.project.models.*;
import com.project.repositories.InputPhaseOneRepository;
import com.project.repositories.PlayerRepository;
import com.project.repositories.RoomRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.Random;

@Service
public class RoomService {

    @Autowired
    RoomRepository roomRepository;
    @Autowired
    PlayerRepository playerRepository;
    @Autowired
    InputPhaseOneRepository inputPhaseOneRepository;
    @Autowired
    PropsService propsService;

    List<String> mockedThemes = Arrays.asList("funny", "creepy", "horror", "friendly", "sad");
    List<String> mockedLocations = Arrays.asList("Egypt", "Wild West", "Ankara", "Somewhere in the North", "London");
    List<String> mockedFinalBosses = Arrays.asList("Dragon", "Earthworm", "Shark", "Old man that turns into 9 tailed fox", "Skeleton");

    public RoomResponseObject accessRoom(RoomDetails roomDetails) {
        String playerName = roomDetails.getName();
        String roomCode = roomDetails.getCode();
        Player newPlayer;

        if (roomRepository.findById(roomCode).isPresent()) {
            Room room = roomRepository.findById(roomCode).get();
            if (room.getGameStarted().equals(true)) {
                return RoomResponseObject.builder().code("GAME_STARTED").build();
            }
            if (room.getPlayers().size() >= 4) {
                return RoomResponseObject.builder().code("ERROR").build();
            }
            Random rand = new Random();
            if (isNameInUse(playerName, roomCode)) {
                playerName = playerName + rand.nextInt(1000);
            }
            newPlayer = buildPlayer(playerName, room);
            playerRepository.save(newPlayer);
            return RoomResponseObject.builder()
                    .name(playerName)
                    .code(roomCode)
                    .isAdmin(newPlayer.isAdmin())
                    .playerPosition(newPlayer.getPlayerPosition())
                    .build();
        }
//        else {
//            Room room = new Room();
//            room.setCode(roomCode);
//            room.setPlayer(new ArrayList<>());
//            roomRepository.save(room); // this part should be done by the game itself
//
//            InputPhaseOne inputPhaseOne = new InputPhaseOne();
//            inputPhaseOne.setRoomCode(room.getCode());
//            inputPhaseOneRepository.saveAndFlush(inputPhaseOne);
//
//        newPlayer = buildPlayer(playerName, room);
//            playerRepository.save(newPlayer);
//        }
//        return RoomResponseObject.builder()
//                .name(playerName)
//                .code(roomCode)
//                .isAdmin(newPlayer.isAdmin())
//                .playerPosition(newPlayer.getPlayerPosition())
//                .build();
        return RoomResponseObject.builder().code("ERROR").build();
    }

    public int gameSize(String code) {
        if (roomRepository.findById(code).isPresent()) {
            Room room = roomRepository.findById(code).get();
            if (room.getPlayers().size() > 0) {
                return room.getPlayers().size();
            }
        }
        return 0;
    }

    public Optional<Room> getRoom(String roomCode) {
        return roomRepository.findById(roomCode);
    }

    private boolean isNameInUse(String name, String roomCode) {
        Optional<Room> room = roomRepository.findById(roomCode);
        if (room.isPresent()) {
            for (Player player : room.get().getPlayers()) {
                if (player.getName().equalsIgnoreCase(name)) {
                    return true;
                }
            }
            return false;
        }
        return false;
    }

    public Room createRoom(String roomCode) {
        Room room = new Room();
        room.setCode(roomCode);
        room.setGameStarted(false);
        return roomRepository.saveAndFlush(room);
    }

    public void lockRoom(String roomCode) {
        Room room = roomRepository.findById(roomCode).get();
        room.setGameStarted(true); // start the game
        roomRepository.saveAndFlush(room);
    }

    public boolean checkIfGameReady(String roomCode) {
        Room room = roomRepository.findById(roomCode).orElse(null);
        if (room != null) {
            int numberOfPlayersInRoom = room.getPlayers().size();
            int numberOfP1Inputs = getTotalCurrentInputs(roomCode);

            if (numberOfP1Inputs == numberOfPlayersInRoom) {
                autocompleteRemainingInputs(roomCode);
                return true;
            }
        }
        return false;
    }

    public void emptyRoom(String roomCode) {
        roomRepository.findById(roomCode).ifPresent(room -> room.setGameStarted(false));
    }

    private Player buildPlayer(String playerName, Room room) {
        Player newPlayer = new Player();
        newPlayer.setAdmin(room.getPlayers().size() <= 0);
        newPlayer.setName(playerName);
        newPlayer.setRoom(room);
        newPlayer.setPlayerPosition((long) room.getPlayers().size());
        return newPlayer;
    }

    private int getTotalCurrentInputs(String roomCode) {
        InputPhaseOne inputPhaseOne = inputPhaseOneRepository.findInputPhaseOneByRoomCodeEquals(roomCode);
        int numberOfInputs = 0;
        if (inputPhaseOne.getTheme() != null) {
            numberOfInputs++;
        }
        if (inputPhaseOne.getLocation() != null) {
            numberOfInputs++;
        }
        if (inputPhaseOne.getElement() != null) {
            numberOfInputs++;
        }
        if (inputPhaseOne.getFinalBoss() != null) {
            numberOfInputs++;
        }

        return numberOfInputs;
    }

    private void autocompleteRemainingInputs(String roomCode) {
        Random rand = new Random();
        InputPhaseOne inputPhaseOne = inputPhaseOneRepository.findInputPhaseOneByRoomCodeEquals(roomCode);
        if (inputPhaseOne.getTheme() == null) {
            inputPhaseOne.setTheme(mockedThemes.get(rand.nextInt(mockedThemes.size())));
        }
        if (inputPhaseOne.getLocation() == null) {
            inputPhaseOne.setLocation(mockedLocations.get(rand.nextInt(mockedLocations.size())));
        }
        if (inputPhaseOne.getElement() == null) {
            List<Props> elements = propsService.getAllElements();
            inputPhaseOne.setElement(elements.get(rand.nextInt(elements.size())).getName());
        }
        if (inputPhaseOne.getFinalBoss() == null) {
            inputPhaseOne.setFinalBoss(mockedFinalBosses.get(rand.nextInt(mockedFinalBosses.size())));
        }

        inputPhaseOneRepository.saveAndFlush(inputPhaseOne);
    }
}
