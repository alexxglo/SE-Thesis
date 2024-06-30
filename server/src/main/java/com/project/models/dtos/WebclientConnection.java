package com.project.models.dtos;

import lombok.Builder;
import lombok.Data;
import java.util.UUID;

@Data
@Builder
public class WebclientConnection {
    String name;
    String code;
    UUID cliendId;
}
