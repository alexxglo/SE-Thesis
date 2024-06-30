package com.project.services;

import com.project.models.Player;
import com.project.models.Room;
import com.project.repositories.PlayerRepository;
import com.project.repositories.RoomRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PlayerService {

    @Autowired
    PlayerRepository playerRepository;
    @Autowired
    RoomRepository roomRepository;

    public List<Player> getPlayersByRoom (String roomCode) {
        Room room = roomRepository.findById(roomCode).orElse(null);
        if (room != null) {
            return playerRepository.getPlayersByRoomEquals(room);
        }
        return null;
    }

    public void emptyRoom(String roomCode) {
        Room room = roomRepository.findById(roomCode).orElse(null);
        if (room != null) {
            playerRepository.deletePlayersByRoomEquals(room);
        }
    }
}
