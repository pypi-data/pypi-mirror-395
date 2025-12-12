/** @odoo-module */

import { registerPatch } from '@mail/model/model_core';

registerPatch({
    name: 'DeleteMessageConfirmView',
    recordMethods: {
        onClickDelete() {
            this._super(...arguments);
            if (this.env?.services?.action?.currentController?.props?.resModel === 'helpdesk.ticket') {
                // Use requestAnimationFrame to prevent conflicts with Owl rendering cycle
                requestAnimationFrame(() => {
                    this.env.bus.trigger('message_update_ev', { message: this });
                });
            }
        },
    },
});
