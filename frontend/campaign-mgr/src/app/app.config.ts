import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideHttpClient } from '@angular/common/http';

import { routes } from './app.routes';
import { ClassRegistry, DataService, DefaultLogSettingsPreferLocal, NgLogService, PropTracker } from 'warskald-ui/services';
import { WsComponentMap } from 'warskald-ui/components';
import { MessageService } from 'primeng/api';
import { AppSettingsConfig } from '@app/models';

NgLogService.initialize(DefaultLogSettingsPreferLocal);
ClassRegistry.initialize(WsComponentMap);
DataService.initialize([]);

export const AppSettings: PropTracker<AppSettingsConfig> = new PropTracker<AppSettingsConfig>({});

AppSettings.setIgnoredKeys([
    'dialogMgr',
    'txSvc',
    'ngZone',
]);

export const appConfig: ApplicationConfig = {
    providers: [
        provideRouter(routes),
        provideAnimations(),
        provideHttpClient(),
        {
            provide: MessageService,
            useValue: new MessageService()
        },
    ],
};
