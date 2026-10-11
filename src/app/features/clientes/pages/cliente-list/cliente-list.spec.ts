import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ClienteList } from './cliente-list';

describe('ClienteList: paginación y baja lógica', () => {
  beforeEach(() => TestBed.configureTestingModule({ imports: [ClienteList], providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()] }));
  afterEach(() => TestBed.inject(HttpTestingController).verify());
  const cliente = { id: 1, dni: '12345678', nombres: 'Ana', apellidos: 'Perez', email: 'ana@test.com', telefono: null, direccion: null, estado: true, fechaCreacion: '', fechaModificacion: null };
  it('envía página, tamaño y orden; filtra sin otra petición', () => {
    const list = TestBed.createComponent(ClienteList).componentInstance;
    const http = TestBed.inject(HttpTestingController);
    list.cambiarTamanio('5');
    const req = http.expectOne(r => r.url.endsWith('/clientes') && r.params.get('tamanio') === '5' && r.params.get('pagina') === '0');
    req.flush({ contenido: [cliente], pagina: 0, tamanio: 5, totalElementos: 6, totalPaginas: 2, primera: true, ultima: false });
    list.filtro.set('PEREZ'); expect(list.filtrados().length).toBe(1);
    list.cambiarPagina(1);
    http.expectOne(r => r.params.get('pagina') === '1').flush({ contenido: [], pagina: 1, tamanio: 5, totalElementos: 6, totalPaginas: 2, primera: false, ultima: true });
    list.ordenar('apellidos');
    http.expectOne(r => r.params.get('direccion') === 'desc' && r.params.get('pagina') === '0').flush({ contenido: [], pagina: 0, totalElementos: 0, totalPaginas: 0, ultima: true });
  });
  it('recarga después de DELETE y conserva la fila inactiva', () => {
    const list = TestBed.createComponent(ClienteList).componentInstance;
    const http = TestBed.inject(HttpTestingController);
    vi.spyOn(window, 'confirm').mockReturnValue(true);
    list.eliminar(cliente);
    http.expectOne(r => r.method === 'DELETE').flush(null, { status: 204, statusText: 'No Content' });
    http.expectOne(r => r.method === 'GET').flush({ contenido: [{ ...cliente, estado: false }], pagina: 0, totalElementos: 1, totalPaginas: 1, ultima: true });
    expect(list.clientes()[0].estado).toBe(false); expect(list.clientes().length).toBe(1);
    vi.restoreAllMocks();
  });
});
