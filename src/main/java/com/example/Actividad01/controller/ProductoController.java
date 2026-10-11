package com.example.Actividad01.controller;

import com.example.Actividad01.dto.ProductoRequestDTO;
import com.example.Actividad01.dto.ProductoResponseDTO;
import com.example.Actividad01.service.service.ProductoService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/api/v1/productos")
public class ProductoController {
    private final ProductoService productoService;

    public ProductoController(ProductoService productoService) {
        this.productoService = productoService;
    }


    @GetMapping
    public ResponseEntity<Iterable<ProductoResponseDTO>> findAll(){
        return ResponseEntity.ok(
                productoService.readAll()
        );
    }



    @GetMapping("/{id}")
    public ResponseEntity<ProductoResponseDTO> findById(@PathVariable Long id){
        return ResponseEntity.ok(
                productoService.read(id)
        );
    }

    @PostMapping
    public ResponseEntity<ProductoResponseDTO> save(@Valid @RequestBody ProductoRequestDTO requestDTO){
        ProductoResponseDTO response= productoService.create(requestDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PutMapping("/{id}")
    public ResponseEntity<ProductoResponseDTO> update( @PathVariable Long id,
            @Valid @RequestBody ProductoRequestDTO requestDTO){
        return ResponseEntity.ok(productoService.update(id, requestDTO));
    }
    @DeleteMapping("/{id}")
    public ResponseEntity<ProductoResponseDTO> delete( @PathVariable Long id){
        productoService.delete(id);
        return ResponseEntity.noContent().build();
    }
}