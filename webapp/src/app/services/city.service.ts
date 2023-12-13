import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { City } from '../post-card/post';

const BASEURL = "http://127.0.0.1:5000/api/v1.0/cities";
const baseHeaders = new HttpHeaders().set('content-type', 'content/json');

@Injectable({
  providedIn: 'root'
})

export class CityService {
  constructor(private http: HttpClient) { 
  }

  getCountries() {
    return this.http.get<string[]>(BASEURL + "/get-countries", { headers: baseHeaders});
  }

  getCities(countryName: string) {
    const params = new HttpParams().set('country', countryName);
    return this.http.get<string[]>(BASEURL, { headers: baseHeaders, params: params});
  }

  getCityByName(cityName: string) {
    return this.http.get<City>(BASEURL + "/" + cityName, { headers: baseHeaders});
  }
}