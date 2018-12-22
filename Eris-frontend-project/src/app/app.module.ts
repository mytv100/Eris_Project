import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {HeadersComponent} from './headers/headers.component'
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import {FormsModule} from '@angular/forms';
import {AgmCoreModule} from '@agm/core';
import {CommonModule} from '@angular/common';
import {ProjectsComponent} from './projects/projects.component';
import {PricingComponent} from './pricing/pricing.component';

@NgModule({
  declarations: [
    AppComponent,
    HeadersComponent,
    ProjectsComponent,
    PricingComponent,
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
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
