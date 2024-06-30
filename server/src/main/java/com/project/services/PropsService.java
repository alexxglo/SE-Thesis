package com.project.services;

import com.project.models.Props;
import com.project.repositories.PropsRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PropsService {

    @Autowired
    PropsRepository propsRepository;

    public List<Props> getProps() {
        return propsRepository.findAll();
    }

    public List<Props> getAllClasses() {
        return propsRepository.findAll().stream().filter(s -> s.getType().equals("class")).toList();
    }

    public List<Props> getAllRaces() {
        return propsRepository.findAll().stream().filter(s -> s.getType().equals("race")).toList();
    }

    public List<Props> getAllWeapons() {
        return propsRepository.findAll().stream().filter(s -> s.getType().equals("weapon")).toList();
    }

    public List<Props> getAllElements() {
        return propsRepository.findAll().stream().filter(s -> s.getType().equals("element")).toList();
    }
}
