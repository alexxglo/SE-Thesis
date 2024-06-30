package com.project.services;

import com.project.models.InputPhaseOne;
import com.project.models.Player;
import com.project.models.Props;
import com.project.models.dtos.CharacterSheet;
import com.project.repositories.InputPhaseOneRepository;
import com.project.repositories.PlayerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Random;

@Service
public class InputService {

    @Autowired
    InputPhaseOneRepository inputPhaseOneRepository;
    @Autowired
    PlayerRepository playerRepository;
    @Autowired
    PropsService propsService;


    public void addToGame(InputPhaseOne input) {
        InputPhaseOne databaseEntry = inputPhaseOneRepository.findInputPhaseOneByRoomCodeEquals(input.getRoomCode());

        if (databaseEntry == null) {
            databaseEntry = new InputPhaseOne();
            databaseEntry.setRoomCode(input.getRoomCode());
        }
        if(input.getElement() != null) {
            databaseEntry.setElement(input.getElement());
        }
        else if (input.getFinalBoss() != null) {
            databaseEntry.setFinalBoss(input.getFinalBoss());
        }
        else if (input.getLocation() != null) {
            databaseEntry.setLocation(input.getLocation());
        }
        else if (input.getTheme() != null) {
            databaseEntry.setTheme(input.getTheme());
        }

        inputPhaseOneRepository.saveAndFlush(databaseEntry);
    }


    public void addCharacter(CharacterSheet characterSheet) {
        List<Player> players = playerRepository.getPlayersByNameEquals(characterSheet.getName());
        List<Props> characterClasses = propsService.getAllClasses();
        List<Props> weapons = propsService.getAllWeapons();
        List<Props> races = propsService.getAllRaces();
        Random rand = new Random();

        if(!players.isEmpty()) {
            Player player = players.stream().filter(s -> s.getRoom().getCode().equals(characterSheet.getRoomCode())).findFirst().get();
            String chClass = characterSheet.getCharacterClass() == null ? characterClasses.get(rand.nextInt(characterClasses.size())).getName() : characterSheet.getCharacterClass();
            String weapon = characterSheet.getWeapon() == null ? weapons.get(rand.nextInt(weapons.size())).getName() : characterSheet.getWeapon();
            String race = characterSheet.getRace() == null ? races.get(rand.nextInt(races.size())).getName() : characterSheet.getRace();

            player.setCharacterClass(chClass);
            player.setWeapon(weapon);
            player.setRace(race);

            playerRepository.saveAndFlush(player);

        }
    }

    public InputPhaseOne getInputP1(String roomCode) {
        return inputPhaseOneRepository.findInputPhaseOneByRoomCodeEquals(roomCode);
    }

    public void empty(String roomCode) {
        inputPhaseOneRepository.deleteInputPhaseOneByRoomCodeEquals(roomCode);
    }

}
