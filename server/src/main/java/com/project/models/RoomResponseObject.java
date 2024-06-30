package com.project.models;

import lombok.Builder;

@Builder
public class RoomResponseObject {
    private String name;
    private String code;
    private boolean isAdmin;
    private Long playerPosition;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public boolean isAdmin() {
        return isAdmin;
    }

    public void setAdmin(boolean admin) {
        isAdmin = admin;
    }

    public Long getPlayerPosition() {
        return playerPosition;
    }

    public void setPlayerPosition(Long playerPosition) {
        this.playerPosition = playerPosition;
    }
}
