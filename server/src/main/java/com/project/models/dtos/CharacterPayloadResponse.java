package com.project.models.dtos;

import java.util.List;

public class CharacterPayloadResponse {
    private List<CharacterPayload> characterSheets;

    public List<CharacterPayload> getCharacterSheets() {
        return characterSheets;
    }

    public void setCharacterSheets(List<CharacterPayload> characterSheets) {
        this.characterSheets = characterSheets;
    }
}
