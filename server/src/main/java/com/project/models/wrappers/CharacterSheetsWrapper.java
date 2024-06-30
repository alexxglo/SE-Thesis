package com.project.models.wrappers;

import com.project.models.dtos.CharacterPayload;

import java.util.List;

public class CharacterSheetsWrapper {
    private List<CharacterPayload> character_sheets;

    // Getters and Setters
    public List<CharacterPayload> getCharacter_sheets() {
        return character_sheets;
    }

    public void setCharacter_sheets(List<CharacterPayload> character_sheets) {
        this.character_sheets = character_sheets;
    }
}
