package com.project.repositories;

import com.project.models.InputPhaseOne;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

@Repository
public interface InputPhaseOneRepository extends JpaRepository<InputPhaseOne, String> {

    InputPhaseOne findInputPhaseOneByRoomCodeEquals(String roomCode);

    @Transactional
    void deleteInputPhaseOneByRoomCodeEquals(String roomCode);
}
