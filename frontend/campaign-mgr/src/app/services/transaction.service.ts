import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { WeakObject } from 'warskald-ui/models';

@Injectable({
    providedIn: 'root',
})
export class TransactionService {

    // #region public properties
    public base_url = 'http://localhost:5000/api/v1/';
    
    // #endregion public properties
    
    
    // #region private properties
    
    // #endregion private properties
    
    
    // #region getters/setters
    
    // #endregion getters/setters
    
    
    // #region standard inputs
    
    // #endregion standard inputs
    
    
    // #region get/set inputs
    
    // #endregion get/set inputs
    
    
    // #region outputs, emitters, and event listeners
    
    // #endregion outputs, emitters, and event listeners
    
    
    // #region viewchildren and contentchildren
    
    // #endregion viewchildren and contentchildren
    
    
    // #region constructor and lifecycle hooks
    
    constructor(
        private http: HttpClient,
    ) {
        
    }

    // #endregion constructor and lifecycle hooks
    
    
    // #region public methods

    public configureHeaders(config?: unknown) {
        let requestOptions = {};

        if (config ?? false) {
            //TODO: convert input into HttpHeaders object
        } 
        else {
            const headerDict = {
                'Content-Type': 'application/json',
                Accept: '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            };

            requestOptions = {
                headers: new Headers(headerDict),
            };
        }

        return requestOptions;
    }
    
    public processQuery(queryData: WeakObject): Promise<unknown> {
        return new Promise((resolve, reject) => {

            this.http.post(this.base_url + 'data', queryData).subscribe({
                next: (response?: unknown) => {
                    if(response == null) {
                        reject('No response from server');
                        return;
                    }
                    if(response) {
                        resolve(response);
                        return;
                    }
                    reject('Invalid response from server');
                },
                error: (error?: unknown) => {
                    reject(error);
                }
            });
        });
    }
    // #endregion public methods
    
    
    // #region protected methods
    
    // #endregion protected methods
    
    
    // #region private methods
    
    // #endregion private methods
    
    
}