package com.project.repositories;

import com.project.models.Player;
import com.project.models.Room;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Repository
public interface PlayerRepository extends JpaRepository<Player, String> {

    List<Player> getPlayersByNameEquals(String name);

    List<Player> getPlayersByRoomEquals(Room room);

    @Transactional
    void deletePlayersByRoomEquals(Room room);
}
