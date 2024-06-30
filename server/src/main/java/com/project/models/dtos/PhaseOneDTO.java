package com.project.models.dtos;

import com.project.models.Player;
import lombok.Builder;
import lombok.Data;

import java.util.List;

@Builder
@Data
public class PhaseOneDTO {
    private String location;
    private String theme;
    private String finalBoss;
    private String element;
    private List<Player> players;
}
