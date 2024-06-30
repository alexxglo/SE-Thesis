package com.project.services;

import com.project.models.InputPhaseOne;
import com.project.models.Player;
import com.project.models.dtos.PhaseOneDTO;
import com.project.models.dtos.WebclientConnection;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CachePut;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class GameService {  // service used to communicate with the game api

    @Autowired
    PlayerService playerService;
    @Autowired
    InputService inputService;

    @CachePut(value = "p1", key ="#roomCode" )
    public PhaseOneDTO postP1GameData(String roomCode) {
        List<Player> players = playerService.getPlayersByRoom(roomCode);
        InputPhaseOne inputPhaseOne = inputService.getInputP1(roomCode);
        return PhaseOneDTO.builder()
                .element(inputPhaseOne.getElement())
                .theme(inputPhaseOne.getTheme())
                .location(inputPhaseOne.getLocation())
                .finalBoss(inputPhaseOne.getFinalBoss())
                .players(players)
                .build();
    }

    @CachePut(value = "webclient", key= "#client.name + #client.code")
    public WebclientConnection cacheWebclientConnection(WebclientConnection client) {
        return client;      // save client connection
    }

}
