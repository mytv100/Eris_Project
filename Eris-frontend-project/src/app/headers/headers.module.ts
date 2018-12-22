import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {HeadersComponent} from './headers.component';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import {FormsModule} from '@angular/forms';
import {AgmCoreModule} from '@agm/core';
import {CommonModule} from '@angular/common';

@NgModule({
  declarations: [
    HeadersComponent,
  ],
  imports: [
    CommonModule,
    BrowserModule,
    NgbModule,
    FormsModule,
    AgmCoreModule.forRoot({
      apiKey: 'YOUR_KEY_HERE'
    }),
  ],
  providers: []
})
export class HeadersModule {
}
