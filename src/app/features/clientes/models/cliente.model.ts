export interface Cliente {
  id: number;
  dni: string;
  nombres: string;
  apellidos: string;
  email: string;
  telefono: string | null;
  direccion: string | null;
  estado: boolean;
  fechaCreacion: string;
  fechaModificacion: string | null;
}

export type ClienteRequest = Omit<Cliente, 'id' | 'fechaCreacion' | 'fechaModificacion'>;
