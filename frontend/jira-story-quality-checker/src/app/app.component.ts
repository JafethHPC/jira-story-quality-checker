import { Component } from '@angular/core';
import { NlpService } from './nlp.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.scss',
})
export class AppComponent {
  textInput: string = '';
  entities: any[] = [];

  constructor(private nlpService: NlpService) {}

  analyzeText() {
    this.nlpService
      .evaluateStoryDescription(this.textInput)
      .subscribe((response) => {
        console.log(response);
        this.entities = response[1];
      });
  }
}
