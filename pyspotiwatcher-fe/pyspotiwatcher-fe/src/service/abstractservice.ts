import { Service } from './service';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';

/**
 * Service astratto, implementa tutti i metodi CRUD inviando request al server di SpringBoot.
 * @param port il port del backend
 * @param type la mappatura del controller di ciascuna entità.
 *
 * @see Service
 *
 * @author Vittorio Valent
 */
export abstract class AbstractService<DTO> implements Service<DTO> {

  type: string;
  port: string = '8080';

  constructor(protected http: HttpClient) {
  }

  getAll(): Observable<DTO[]> {
    return this.http.get<DTO[]>(environment.APIEndpoint + this.type + '/list');
  }

  read(id: number): Observable<DTO> {
    return this.http.get<DTO>(environment.APIEndpoint + this.type + '/read/' + id);
  }

  delete(id: string): Observable<any> {
    return this.http.delete(environment.APIEndpoint + this.type + '/delete/' + id);
  }

  insert(dto: DTO): Observable<any> {
    return this.http.post(environment.APIEndpoint + this.type + '/insert', dto);
  }

  update(dto: DTO): Observable<DTO> {
    return this.http.put<DTO>(environment.APIEndpoint + this.type + '/update', dto);

  }

}
