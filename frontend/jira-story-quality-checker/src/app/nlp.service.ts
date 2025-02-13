import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class NlpService {
  private apiUrl = 'http://127.0.0.1:8000/evaluate';

  constructor(private http: HttpClient) {}

  evaluateStoryDescription(description: string): Observable<any> {
    let x: any;
    this.http.post<any>(this.apiUrl, { description }).subscribe((res) => {
      console.log(res);
      x = res;
    });
    return x;
  }
}
