import { Component, inject, input, OnInit, signal } from '@angular/core';
import { NonNullableFormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { ProductoService } from '../../services/producto-service';
import { CategoriaService } from '../../../categorias/services/categoria-service';
import { Categoria } from '../../../categorias/models/categoria.model';
import { mensajeError } from '../../../../core/utils/http-error';
@Component({ selector: 'app-producto-form', imports: [ReactiveFormsModule, RouterLink], templateUrl: './producto-form.html' })
export class ProductoForm implements OnInit {
  private readonly fb = inject(NonNullableFormBuilder);
  private readonly service = inject(ProductoService);
  private readonly categoriaService = inject(CategoriaService);
  private readonly router = inject(Router);
  readonly id = input<string>();
  readonly categorias = signal<Categoria[]>([]);
  readonly cargando = signal(true);
  readonly cargaFallida = signal(false);
  readonly guardando = signal(false);
  readonly error = signal('');
  readonly form = this.fb.group({ nombre: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(150), Validators.pattern(/.*\S.*/)]], precio: [0.01, [Validators.required, Validators.min(0.01), Validators.pattern(/^\d+(\.\d{1,2})?$/)]], stock: [0, [Validators.required, Validators.min(0), Validators.pattern(/^\d+$/)]], categoria: this.fb.control<number | null>(null, Validators.required), estado: [true] });
  ngOnInit() {
    const categorias = this.categoriaService.listar();
    if (this.id()) {
      forkJoin({ categorias, producto: this.service.obtener(Number(this.id())) }).subscribe({ next: ({ categorias, producto: p }) => { this.categorias.set(categorias); this.form.setValue({ nombre:p.nombre, precio:p.precio, stock:p.stock, categoria:p.categoriaId, estado:p.estado }); this.cargando.set(false); }, error: e => this.fallo(e) });
    } else categorias.subscribe({ next: c => { this.categorias.set(c); this.cargando.set(false); }, error: e => this.fallo(e) });
  }
  private fallo(e: Parameters<typeof mensajeError>[0]) { this.cargando.set(false); this.cargaFallida.set(true); this.error.set(mensajeError(e)); }
  guardar() {
    if (this.cargando() || this.cargaFallida() || this.guardando()) return;
    this.form.controls.nombre.setValue(this.form.controls.nombre.value.trim());
    if (this.form.invalid) { this.form.markAllAsTouched(); return; }
    const v = this.form.getRawValue(); const dto = { ...v, categoria: Number(v.categoria), precio:Number(v.precio), stock:Number(v.stock) };
    this.guardando.set(true); this.error.set('');
    (this.id() ? this.service.actualizar(Number(this.id()), dto) : this.service.crear(dto)).subscribe({ next: () => this.router.navigate(['/productos'], { queryParams:{guardado:1} }), error: e => { this.error.set(mensajeError(e)); this.guardando.set(false); } });
  }
}
