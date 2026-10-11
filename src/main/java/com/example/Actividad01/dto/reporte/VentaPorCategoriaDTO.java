package com.example.Actividad01.dto.reporte;

import java.math.BigDecimal;

public record VentaPorCategoriaDTO(
        Long categoriaId,
        String nombreCategoria,
        Long cantidadTotal,
        BigDecimal montoTotal
) {
}
