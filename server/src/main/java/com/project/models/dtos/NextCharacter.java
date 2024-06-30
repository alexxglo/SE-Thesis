package com.project.models.dtos;

import lombok.Builder;
import lombok.Data;

public class NextCharacter {
    private String name;
    private String room;

    public NextCharacter(){};

    public NextCharacter(String name, String room) {
        this.name = name;
        this.room = room;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getRoom() {
        return room;
    }

    public void setRoom(String room) {
        this.room = room;
    }
}
