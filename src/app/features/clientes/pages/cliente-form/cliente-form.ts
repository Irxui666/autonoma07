import { Component, inject, input, OnInit, signal } from '@angular/core';
import { NonNullableFormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ClienteService } from '../../services/cliente-service';
import { ClienteRequest } from '../../models/cliente.model';
import { mensajeError, erroresDeValidacion } from '../../../../core/utils/http-error';

@Component({ selector: 'app-cliente-form', imports: [ReactiveFormsModule, RouterLink], templateUrl: './cliente-form.html' })
export class ClienteForm implements OnInit {
  private readonly fb = inject(NonNullableFormBuilder);
  private readonly service = inject(ClienteService);
  private readonly router = inject(Router);
  readonly id = input<string>();
  readonly cargando = signal(false);
  readonly cargaFallida = signal(false);
  readonly guardando = signal(false);
  readonly error = signal('');
  readonly erroresServidor = signal<Record<string, string>>({});
  readonly campos = [
    { key: 'dni', label: 'DNI', type: 'text', hint: 'Exactamente 8 dígitos.' },
    { key: 'nombres', label: 'Nombres', type: 'text', hint: 'Entre 2 y 100 caracteres.' },
    { key: 'apellidos', label: 'Apellidos', type: 'text', hint: 'Entre 2 y 100 caracteres.' },
    { key: 'email', label: 'Correo electrónico', type: 'email', hint: 'Correo válido de hasta 150 caracteres.' },
    { key: 'telefono', label: 'Teléfono opcional', type: 'tel', hint: 'Si se proporciona, debe tener 9 dígitos.' },
    { key: 'direccion', label: 'Dirección opcional', type: 'text', hint: 'Hasta 250 caracteres.' },
  ] as const;
  readonly form = this.fb.group({
    dni: ['', [Validators.required, Validators.pattern(/^\d{8}$/)]],
    nombres: ['', [Validators.required, Validators.minLength(2), Validators.maxLength(100), Validators.pattern(/.*\S.*/)]],
    apellidos: ['', [Validators.required, Validators.minLength(2), Validators.maxLength(100), Validators.pattern(/.*\S.*/)]],
    email: ['', [Validators.required, Validators.email, Validators.maxLength(150)]],
    telefono: ['', [Validators.pattern(/^\d{9}$/)]],
    direccion: ['', [Validators.maxLength(250)]],
    estado: [true],
  });
  ngOnInit() {
    const id = this.id(); if (!id) return;
    this.cargando.set(true);
    this.service.obtener(Number(id)).subscribe({ next: c => { this.form.setValue({ dni:c.dni, nombres:c.nombres, apellidos:c.apellidos, email:c.email, telefono:c.telefono ?? '', direccion:c.direccion ?? '', estado:c.estado }); this.cargando.set(false); }, error: e => { this.cargando.set(false); this.cargaFallida.set(true); this.error.set(mensajeError(e)); } });
  }
  guardar() {
    if (this.guardando() || this.cargando() || this.cargaFallida()) return;
    for (const field of this.campos) this.form.controls[field.key].setValue(this.form.controls[field.key].value.trim());
    if (this.form.invalid) { this.form.markAllAsTouched(); return; }
    const v = this.form.getRawValue();
    const dto: ClienteRequest = { ...v, telefono: v.telefono || null, direccion: v.direccion || null };
    this.guardando.set(true); this.error.set(''); this.erroresServidor.set({});
    const request = this.id() ? this.service.actualizar(Number(this.id()), dto) : this.service.crear(dto);
    request.subscribe({ next: () => this.router.navigate(['/clientes'], { queryParams: { guardado: 1 } }), error: e => { this.guardando.set(false); this.error.set(mensajeError(e)); this.erroresServidor.set(erroresDeValidacion(e)); } });
  }
}
