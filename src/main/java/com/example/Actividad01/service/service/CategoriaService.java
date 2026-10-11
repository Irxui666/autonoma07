package com.example.Actividad01.service.service;

import com.example.Actividad01.dto.CategoriaRequestDTO;
import com.example.Actividad01.dto.CategoriaResponseDTO;
import com.example.Actividad01.service.generic.CrudService;
import org.springframework.stereotype.Service;

@Service

public interface CategoriaService extends CrudService<CategoriaRequestDTO, CategoriaResponseDTO, Long> {
}
