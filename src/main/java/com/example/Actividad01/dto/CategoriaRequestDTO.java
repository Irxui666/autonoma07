package com.example.Actividad01.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@AllArgsConstructor
@Getter
@Setter
@NoArgsConstructor
public class CategoriaRequestDTO {
    @NotBlank(message = "El nombre de la categoria es obligatorio")
    @Size(
            min = 3,
            max = 50,
            message = "El nombre de la categoria entre 3 y 50 caracteres"
    )
    private String nombre;

    @Size(
            max = 200,
            message = "La descripcion no debe superar los 200 caracteres"
    )
    private String descripcion;

    @NotNull(message = "El estado es obligatorio")
    private Boolean estado;
}
