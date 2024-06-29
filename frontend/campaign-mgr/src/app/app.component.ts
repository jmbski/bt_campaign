import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, NgZone } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { AppDeviceInfo, LayoutChangeObserver$ } from 'warskald-ui/common';
import { MessageService, PrimeNGConfig } from 'primeng/api';
import { DeviceDetectorService } from 'ngx-device-detector';
import { DataService, DialogManagerService, NavigationService, NgLogService, ToastService, UpdaterFunctionMap } from 'warskald-ui/services';
import { ToastModule } from 'primeng/toast';
import { BlockableUiComponent, PullToRefreshComponent } from 'warskald-ui/components';
//import { getCurrentLangConfig, TransactionService } from '@app/services';
//import { AppSettings } from './app.config';
//import { AppSettingsConfig } from './models/app-settings';
import { isNumber } from 'warskald-ui/type-guards';
import { TransactionService } from '@app/services';
import { AppSettings } from './app.config';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [
        BlockableUiComponent,
        CommonModule,
        PullToRefreshComponent,
        RouterOutlet,
        ToastModule,
    ],
    providers: [
        MessageService,
        TransactionService,
    ],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss'
})
export class AppComponent {

    public resizeObserver?: ResizeObserver;

    // #region public properties
    
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
        public cd: ChangeDetectorRef,
        public logSvc: NgLogService,
        private txSvc: TransactionService,
        private primengConfig: PrimeNGConfig,
        private deviceDetector: DeviceDetectorService,
        private navSvc: NavigationService,
        private dialogMgr: DialogManagerService,
        private ngZone: NgZone,
        private messageService: MessageService,
        private router: Router,
    ) {
        NavigationService.initialize(router);
        ToastService.messageService = this.messageService;
        
        //AppDeviceInfo.isDesktop = this.deviceDetector.isDesktop();
        AppDeviceInfo.isMobile = this.deviceDetector.isMobile();
        AppDeviceInfo.isTablet = this.deviceDetector.isTablet();

        AppSettings.setValue('dialogMgr', dialogMgr);
        AppSettings.setValue('txSvc', txSvc);
        AppSettings.setValue('ngZone', ngZone);
        
    }

    ngOnInit() {
        this.primengConfig.ripple = true;
        this.primengConfig.zIndex = {

            modal: 4000,
            overlay: 3005,
            menu: 3006,
            tooltip: 4000
        };

        this.primengConfig.zIndex = {
            modal: 11100,    // dialog, sidebar
            overlay: 10000,  // dropdown, overlaypanel
            menu: 11000,     // overlay menus
            tooltip: 11050  // tooltip
        };

        this.txSvc.processQuery({
            entity: 'User',
            action: 'get_multiple',
            data: {}
        })
            .then((response) => {
                console.log(response);
            })
            .catch((error) => {
                console.error(error);
            });
    }

    ngAfterViewInit() {

        this.resizeObserver = new ResizeObserver((data: ResizeObserverEntry[]) => {
            const width: number = data[0].contentRect.width;
            const height: number = data[0].contentRect.height;
            
            if (width <= 761 || height <= 600) {
                AppDeviceInfo.isMobile = true;
            }
            else {
                AppDeviceInfo.isMobile = false;
            }
            
            LayoutChangeObserver$.next();
                
            const appTopNav: HTMLElement = <HTMLElement>document.querySelector('.app-top-nav');
            if(appTopNav) {
                const appTopNavShadow: HTMLElement = <HTMLElement>document.querySelector('.app-top-nav-shadow');
                if(appTopNavShadow) {
                    appTopNavShadow.style.height = `${appTopNav.offsetHeight}px`;
                }
            }
            this.cd.detectChanges();
        });
        /*  */
        this.resizeObserver.observe(document.body);
        // GlobalResizeObserver.next(this.resizeObserver);
        
    }
    // #endregion constructor and lifecycle hooks
    
    
    // #region public methods
    
    // #endregion public methods
    
    
    // #region protected methods
    
    // #endregion protected methods
    
    
    // #region private methods
    
    // #endregion private methods
    
    
}
