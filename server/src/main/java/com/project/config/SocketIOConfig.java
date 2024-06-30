package com.project.config;

import lombok.extern.log4j.Log4j2;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;

import com.corundumstudio.socketio.Configuration;
import com.corundumstudio.socketio.SocketIOServer;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.CrossOrigin;

@CrossOrigin
@Component
@Log4j2
public class SocketIOConfig {
    @Value("${socket-server.host}")
    private String SOCKETHOST;
    @Value("${socket-server.port}")
    private int SOCKETPORT;

    public SocketIOConfig() {
    }

    @Bean
    public SocketIOServer socketIOServer() {
        Configuration config = new Configuration();
        config.setHostname(SOCKETHOST);
        config.setPort(SOCKETPORT);
        return new SocketIOServer(config);
    }
}
