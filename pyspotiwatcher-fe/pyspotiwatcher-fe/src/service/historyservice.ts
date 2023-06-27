import {Injectable} from '@angular/core';
import {AbstractService} from './abstractservice';
import {HttpClient, HttpHeaders, HttpRequest, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import {environment} from './../environments/environment';
import {HistoryRowDTO} from "../dto/historyrow";

/**
 * I service sono decorati da @Injectable.
 * Qui trovate, oltre ai metodi ereditati dall'Abstract,
 *  il metodo per il login (in mirror con il backend).
 *
 * @author Vittorio Valent
 *
 * @see AbstractService
 */
@Injectable({
  providedIn: 'root'
})
export class HistoryService extends AbstractService<HistoryRowDTO> {

  constructor(http: HttpClient) {
    super(http);
    this.port = '8080';
    this.type = 'history'
  }

}
