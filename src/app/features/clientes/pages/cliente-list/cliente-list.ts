import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ClienteService } from '../../services/cliente-service';
import { Cliente } from '../../models/cliente.model';
import { mensajeError } from '../../../../core/utils/http-error';

@Component({ selector: 'app-cliente-list', imports: [RouterLink], templateUrl: './cliente-list.html' })
export class ClienteList implements OnInit {
  private readonly service = inject(ClienteService);
  private readonly route = inject(ActivatedRoute);
  readonly pagina = signal(0);
  readonly tamanio = signal(10);
  readonly ordenarPor = signal<'dni' | 'apellidos'>('apellidos');
  readonly direccion = signal<'asc' | 'desc'>('asc');
  readonly totalPaginas = signal(0);
  readonly totalElementos = signal(0);
  readonly ultima = signal(true);
  readonly clientes = signal<Cliente[]>([]);
  readonly cargando = signal(false);
  readonly eliminando = signal(false);
  readonly error = signal('');
  readonly exito = signal('');
  readonly filtro = signal('');
  readonly filtrados = computed(() => {
    const q = this.filtro().trim().toLocaleLowerCase();
    return this.clientes().filter(c => `${c.dni} ${c.nombres} ${c.apellidos} ${c.email}`.toLocaleLowerCase().includes(q));
  });
  ngOnInit() { if (this.route.snapshot.queryParamMap.has('guardado')) this.exito.set('Cliente guardado correctamente.'); this.cargar(); }
  cargar() {
    this.cargando.set(true); this.error.set('');
    this.service.listar(this.pagina(), this.tamanio(), this.ordenarPor(), this.direccion()).subscribe({ next: data => { this.clientes.set(data.contenido); this.pagina.set(data.pagina); this.totalPaginas.set(data.totalPaginas); this.totalElementos.set(data.totalElementos); this.ultima.set(data.ultima); this.cargando.set(false); }, error: e => { this.error.set(mensajeError(e)); this.cargando.set(false); } });
  }
  cambiarPagina(delta: number) { this.pagina.update(p => p + delta); this.cargar(); }
  cambiarTamanio(valor: string) { this.tamanio.set(Number(valor)); this.pagina.set(0); this.cargar(); }
  ordenar(campo: 'dni' | 'apellidos') {
    this.direccion.set(this.ordenarPor() === campo && this.direccion() === 'asc' ? 'desc' : 'asc');
    this.ordenarPor.set(campo); this.pagina.set(0); this.cargar();
  }
  eliminar(cliente: Cliente) {
    if (!confirm(`¿Dar de baja al cliente ${cliente.nombres} ${cliente.apellidos}?`)) return;
    this.eliminando.set(true); this.error.set(''); this.exito.set('');
    this.service.eliminar(cliente.id).subscribe({ next: () => { this.eliminando.set(false); this.exito.set('Cliente dado de baja.'); this.cargar(); }, error: e => { this.eliminando.set(false); this.error.set(mensajeError(e)); } });
  }
}
