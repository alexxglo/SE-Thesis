package com.project.models;

import jakarta.persistence.*;

@Entity
@Table(name = "input_phase_one")
public class InputPhaseOne {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column
    private String location;
    @Column
    private String theme;
    @Column
    private String finalBoss;
    @Column
    private String element;
    @Column
    private String roomCode;

    public InputPhaseOne() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getTheme() {
        return theme;
    }

    public void setTheme(String theme) {
        this.theme = theme;
    }

    public String getFinalBoss() {
        return finalBoss;
    }

    public void setFinalBoss(String finalBoss) {
        this.finalBoss = finalBoss;
    }

    public String getElement() {
        return element;
    }

    public void setElement(String element) {
        this.element = element;
    }

    public void setRoomCode(String room) {
        this.roomCode = room;
    }

    public String getRoomCode() {
        return roomCode;
    }
}
