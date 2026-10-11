package com.example.Actividad01.controller;

import com.example.Actividad01.dto.CategoriaRequestDTO;
import com.example.Actividad01.dto.CategoriaResponseDTO;
import com.example.Actividad01.entity.Categoria;
import com.example.Actividad01.service.service.CategoriaService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/api/v1/categorias")
public class CategoriaController {
    private final CategoriaService categoriaService;

    public CategoriaController(CategoriaService categoriaService) {
        this.categoriaService = categoriaService;
    }


    @GetMapping
    public ResponseEntity<Iterable<CategoriaResponseDTO>> findAll(){
        return ResponseEntity.ok(
                categoriaService.readAll()
        );
    }



    @GetMapping("/{id}")
    public ResponseEntity<CategoriaResponseDTO> findById(@PathVariable Long id){
        return ResponseEntity.ok(
                categoriaService.read(id)
        );
    }

    @PostMapping
    public ResponseEntity<CategoriaResponseDTO> save(@Valid @RequestBody CategoriaRequestDTO requestDTO){
        CategoriaResponseDTO response= categoriaService.create(requestDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PutMapping("/{id}")
    public ResponseEntity<CategoriaResponseDTO> update( @PathVariable Long id,
            @Valid @RequestBody CategoriaRequestDTO requestDTO){
        return ResponseEntity.ok(categoriaService.update(id, requestDTO));
    }
    @DeleteMapping("/{id}")
    public ResponseEntity<CategoriaResponseDTO> delete( @PathVariable Long id){
        categoriaService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
