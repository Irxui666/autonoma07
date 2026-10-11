package com.example.Actividad01;
import com.example.Actividad01.entity.Cliente;
import com.example.Actividad01.exception.ReglaNegocioException;
import com.example.Actividad01.repository.ClienteRepository;
import com.example.Actividad01.service.impl.ClienteServiceImpl;
import org.junit.jupiter.api.Test;
import java.util.Optional;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
class ClienteServiceRulesTest {
    @Test void bajaLogicaYConflictoAlRepetir() {
        var repository = mock(ClienteRepository.class);
        var service = new ClienteServiceImpl(repository);
        var cliente = new Cliente(); cliente.setEstado(true);
        when(repository.findById(1L)).thenReturn(Optional.of(cliente));
        service.delete(1L);
        assertFalse(cliente.getEstado());
        verify(repository).save(cliente);
        verify(repository, never()).delete(any());
        assertThrows(ReglaNegocioException.class, () -> service.delete(1L));
        verify(repository, times(1)).save(cliente);
    }
    @Test void rechazaCampoDeOrdenNoPermitido() {
        var repository = mock(ClienteRepository.class);
        var service = new ClienteServiceImpl(repository);
        assertThrows(ReglaNegocioException.class, () -> service.listar(0, 10, "password", "asc"));
        verifyNoInteractions(repository);
    }
}
