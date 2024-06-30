package com.project.models.dtos;

import java.util.List;

public class CharacterPayload {

    private String name;
    private String characterClass;
    private List<Spell> spells;
    private String proficiencies;
    private int level;
    private int xp;
    private int xpToNextLevel;
    private String inventory;
    private MainWeapon mainWeapon;
    private String roomCode;

    public String getCharacterClass() {
        return characterClass;
    }

    public void setCharacterClass(String className) {
        this.characterClass = className;
    }

    public String getInventory() {
        return inventory;
    }

    public void setInventory(String inventory) {
        this.inventory = inventory;
    }

    public int getLevel() {
        return level;
    }

    public void setLevel(int level) {
        this.level = level;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getProficiencies() {
        return proficiencies;
    }

    public void setProficiencies(String proficiencies) {
        this.proficiencies = proficiencies;
    }

    public int getXp() {
        return xp;
    }

    public void setXp(int xp) {
        this.xp = xp;
    }

    public int getXpToNextLevel() {
        return xpToNextLevel;
    }

    public void setXpToNextLevel(int xpToNextLevel) {
        this.xpToNextLevel = xpToNextLevel;
    }

    public MainWeapon getMainWeapon() {
        return mainWeapon;
    }

    public void setMainWeapon(MainWeapon mainWeapon) {
        this.mainWeapon = mainWeapon;
    }

    public List<Spell> getSpells() {
        return spells;
    }

    public void setSpells(List<Spell> spells) {
        this.spells = spells;
    }

    public String getRoomCode() {
        return roomCode;
    }

    public void setRoomCode(String roomCode) {
        this.roomCode = roomCode;
    }
}
