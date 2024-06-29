import { NgZone } from '@angular/core';
import { TransactionService } from '@app/services';
import { DialogManagerService } from 'warskald-ui/services';

export interface AppSettingsConfig {
    dialogMgr?: DialogManagerService;
    txSvc?: TransactionService;
    ngZone?: NgZone;
}