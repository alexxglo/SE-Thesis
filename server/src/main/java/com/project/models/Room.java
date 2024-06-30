package com.project.models;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

import java.util.List;

@Entity
@Table(name="rooms")
public class Room {
    @Id
    private String code;

    private Boolean isGameStarted;

    @OneToMany(mappedBy = "room")
    private List<Player> players;

    public Room() {
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public List<Player> getPlayers() {
        return players;
    }

    public void setPlayer(List<Player> players) {
        this.players = players;
    }

    public Boolean getGameStarted() {
        return isGameStarted;
    }

    public void setGameStarted(Boolean gameStarted) {
        isGameStarted = gameStarted;
    }
}
