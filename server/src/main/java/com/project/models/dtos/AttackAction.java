package com.project.models.dtos;

import lombok.Builder;
import lombok.Data;

public class AttackAction {
    private String name;
    private String ability;
    private String damage;
    private String room;

    public AttackAction() {

    }
    public AttackAction(String name, String ability, String damage, String room) {
        this.name = name;
        this.ability = ability;
        this.damage = damage;
        this.room = room;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAbility() {
        return ability;
    }

    public void setAbility(String ability) {
        this.ability = ability;
    }

    public String getDamage() {
        return damage;
    }

    public void setDamage(String damage) {
        this.damage = damage;
    }

    public String getRoom() {
        return room;
    }

    public void setRoom(String room) {
        this.room = room;
    }
}
