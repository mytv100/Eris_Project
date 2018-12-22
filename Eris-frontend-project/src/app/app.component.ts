import {AfterViewInit, Component, OnDestroy, OnInit} from '@angular/core';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy, AfterViewInit {
  private fragment: string;

  title = 'abscessed'


  ngOnInit() {
  }

  ngOnDestroy() {

  }

  ngAfterViewInit() {

  }
}
