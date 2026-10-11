package com.example.Actividad01.service.service;
import com.example.Actividad01.dto.reporte.ProductoMasVendidoDTO;
import com.example.Actividad01.dto.reporte.VentaPorCategoriaDTO;
import com.example.Actividad01.service.generic.CrudService;

import java.time.LocalDate;
import java.util.List;

public interface ReporteService {
    List<VentaPorCategoriaDTO> ventasPorCategoria(
            LocalDate desde,
            LocalDate hasta);

    List<ProductoMasVendidoDTO> productosMasVendidos(
            LocalDate desde,
            LocalDate hasta);
}
