import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ClienteForm } from './cliente-form';

describe('ClienteForm: contrato tarea05', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [ClienteForm], providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()],
  }));
  afterEach(() => TestBed.inject(HttpTestingController).verify());
  it('rechaza DNI y teléfono inválidos sin enviar datos', () => {
    const form = TestBed.createComponent(ClienteForm).componentInstance;
    form.form.setValue({ dni: '123', nombres: 'Ana', apellidos: 'Perez', email: 'ana@test.com', telefono: '123', direccion: '', estado: true });
    form.guardar();
    expect(form.form.invalid).toBe(true);
    TestBed.inject(HttpTestingController).expectNone('/api/v1/clientes');
  });
  it('envía campos opcionales vacíos como null y muestra conflictos', () => {
    const form = TestBed.createComponent(ClienteForm).componentInstance;
    form.form.setValue({ dni: '12345678', nombres: ' Ana ', apellidos: 'Perez', email: 'ana@test.com', telefono: '', direccion: '', estado: true });
    form.guardar();
    const request = TestBed.inject(HttpTestingController).expectOne('/api/v1/clientes');
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual({ dni: '12345678', nombres: 'Ana', apellidos: 'Perez', email: 'ana@test.com', telefono: null, direccion: null, estado: true });
    request.flush({ message: 'DNI duplicado' }, { status: 409, statusText: 'Conflict' });
    expect(form.guardando()).toBe(false);
    expect(form.error()).toContain('DNI duplicado');
  });
});
