package com.example.Actividad01.dto;

import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;
@AllArgsConstructor
@Getter
@Setter
@NoArgsConstructor
public class ProductoRequestDTO {
    @NotBlank(message = "El nombre del producto es obligatorio")
    @Size(
            min = 3,
            max = 150,
            message = "El nombre de la categoria entre 3 y 150 caracteres"
    )
    private String nombre;
    @NotNull(message = "El precio del producto es obligatorio")
    @DecimalMin(
            value = "0.01",
            message = "El precio debe ser mayor que cero"
    )
    private BigDecimal precio;
    @NotNull(message = "El stock es obligatorio")
    @Min(
            value = 0,
            message = "El stock no puede ser negativo"
    )
    private Integer stock;
    @NotNull(message = "El estado es obligatorio")
    private Boolean estado;
    @NotNull(message = "La categoria es obligatoria")
    @Positive(message = "El identificador de categoria debe ser valido")
    private Long categoria;
}
