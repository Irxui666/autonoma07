package com.example.Actividad01.repository;

import com.example.Actividad01.dto.reporte.ProductoMasVendidoDTO;
import com.example.Actividad01.dto.reporte.VentaPorCategoriaDTO;
import com.example.Actividad01.entity.Venta;
import com.example.Actividad01.enums.EstadoVenta;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.data.domain.Sort;
import java.time.LocalDateTime;
import java.util.List;

public interface VentaRepository extends JpaRepository<Venta, Long> {
    @org.springframework.data.jpa.repository.Lock(jakarta.persistence.LockModeType.PESSIMISTIC_WRITE)
    @Query("select v from Venta v where v.id = :id")
    java.util.Optional<Venta> bloquearPorId(@Param("id") Long id);

    @Query("""
            select v from Venta v
            where (:clienteId is null or v.cliente.id = :clienteId)
              and (:estado is null or v.estado = :estado)
              and (:desde is null or v.fecha >= :desde)
              and (:hasta is null or v.fecha <= :hasta)
            """)
    org.springframework.data.domain.Page<Venta> buscarPagina(
            @Param("clienteId") Long clienteId, @Param("estado") EstadoVenta estado,
            @Param("desde") LocalDateTime desde, @Param("hasta") LocalDateTime hasta,
            org.springframework.data.domain.Pageable pageable);
    @Query("""
            select distinct v
            from Venta v
            left join fetch v.cliente c
            left join fetch v.detalles d
            left join fetch d.producto p
            where (:clienteId is null or c.id = :clienteId)
              and (:estado    is null or v.estado = :estado)
              and (:desde     is null or v.fecha >= :desde)
              and (:hasta     is null or v.fecha <= :hasta)
            """)
    List<Venta> buscar(
            @Param("clienteId") Long clienteId,
            @Param("estado") EstadoVenta estado,
            @Param("desde") LocalDateTime desde,
            @Param("hasta") LocalDateTime hasta,
            Sort sort);
    @Query("""
            select new com.example.Actividad01.dto.reporte.VentaPorCategoriaDTO(
                       cat.id,
                       cat.nombre,
                       sum(d.cantidad),
                       sum(d.subtotal))
            from DetalleVenta d
            join d.venta v
            join d.producto p
            join p.categoria cat
            where v.estado = com.example.Actividad01.enums.EstadoVenta.REGISTRADA
              and (:desde is null or v.fecha >= :desde)
              and (:hasta is null or v.fecha <= :hasta)
            group by cat.id, cat.nombre
            order by sum(d.subtotal) desc
            """)
    List<VentaPorCategoriaDTO> reporteVentasPorCategoria(
            @Param("desde") LocalDateTime desde,
            @Param("hasta") LocalDateTime hasta);

    @Query("""
            select new com.example.Actividad01.dto.reporte.ProductoMasVendidoDTO(
                       p.id,
                       p.nombre,
                       cat.nombre,
                       sum(d.cantidad),
                       sum(d.subtotal))
            from DetalleVenta d
            join d.venta v
            join d.producto p
            join p.categoria cat
            where v.estado = com.example.Actividad01.enums.EstadoVenta.REGISTRADA
              and (:desde is null or v.fecha >= :desde)
              and (:hasta is null or v.fecha <= :hasta)
            group by p.id, p.nombre, cat.nombre
            order by sum(d.cantidad) desc
            """)
    List<ProductoMasVendidoDTO> reporteProductosMasVendidos(
            @Param("desde") LocalDateTime desde,
            @Param("hasta") LocalDateTime hasta);

}
