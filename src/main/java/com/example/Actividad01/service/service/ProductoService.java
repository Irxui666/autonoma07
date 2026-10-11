package com.example.Actividad01.service.service;

import com.example.Actividad01.dto.ProductoRequestDTO;
import com.example.Actividad01.dto.ProductoResponseDTO;
import com.example.Actividad01.service.generic.CrudService;

public interface ProductoService extends CrudService<ProductoRequestDTO, ProductoResponseDTO, Long> {
}
