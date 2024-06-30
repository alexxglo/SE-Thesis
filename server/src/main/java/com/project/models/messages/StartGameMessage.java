package com.project.models.messages;

import lombok.Data;

@Data
public class StartGameMessage {

    private String room;

    private int playerNumber;

    public StartGameMessage() {

    };
    public StartGameMessage(int playerNumber) {
        this.playerNumber = playerNumber;
    }

}
