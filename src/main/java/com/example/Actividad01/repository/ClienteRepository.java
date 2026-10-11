package com.example.Actividad01.repository;

import com.example.Actividad01.entity.Cliente;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ClienteRepository extends JpaRepository<Cliente, Long> {
    boolean existsByDni(String dni);
    boolean existsByEmailIgnoreCase(String email);

    boolean existsByDniAndIdNot(String dni, Long id);
    boolean existsByEmailIgnoreCaseAndIdNot(String email, Long id);
}
