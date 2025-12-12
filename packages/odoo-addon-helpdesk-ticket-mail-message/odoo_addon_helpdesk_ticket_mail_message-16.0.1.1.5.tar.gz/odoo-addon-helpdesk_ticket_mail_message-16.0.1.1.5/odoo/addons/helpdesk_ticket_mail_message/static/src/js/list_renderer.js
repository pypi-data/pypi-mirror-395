/** @odoo-module */

import { registry } from '@web/core/registry';
import { useEffect, useState } from "@odoo/owl";
import { ListRenderer } from '@web/views/list/list_renderer';
import { X2ManyField } from '@web/views/fields/x2many/x2many_field';


const MESSAGE_TYPE_MAIL_ACTION_MAP = {
    note: "mail_compose_message_action_note_open",
    email_received: "mail_compose_message_action_readonly",
    email_sent: "mail_compose_message_action_readonly",
    email_scheduled: "mail_compose_message_action_reschedule",
};


export class ListRendererMailIcon extends ListRenderer {
    setup() {
        super.setup();

        this.filterButtons = {
            emailSent: { icon: 'fa-long-arrow-left color-red', active: false },
            emailReceived: { icon: 'fa-long-arrow-right color-black', active: false },
            note: { icon: 'fa-file-text-o color-green', active: false }
        };

        // Use reactive state instead of direct DOM manipulation
        this.messageState = useState({
            needsRefresh: false,
            isDestroyed: false
        });

        useEffect(() => {
            if (!this.messageState.isDestroyed && this.tableRef?.el) {
                this.setupFilterButtonsSafely();
                this.renderMailIconsSafely();
            }
        });

        // Safer bus event handling with component lifecycle checks
        this._messageUpdateHandler = this._onMessageContentUpdated.bind(this);
        this.env.bus.addEventListener("message_update_ev", this._messageUpdateHandler);
    }

    willUnmount() {
        // Mark component as destroyed to prevent further DOM operations
        if (this.messageState) {
            this.messageState.isDestroyed = true;
        }

        // Clean up bus event listeners to prevent memory leaks
        if (this._messageUpdateHandler) {
            this.env.bus.removeEventListener("message_update_ev", this._messageUpdateHandler);
        }

        super.willUnmount && super.willUnmount();
    }

    async _onMessageContentUpdated({ message }) {
        try {
            // Enhanced safety checks to prevent race conditions
            if (this.messageState?.isDestroyed ||
                !this.tableRef?.el ||
                !this.props?.list?.model ||
                !this.__owl__?.fiber?.isRoot) {
                return;
            }

            // Use requestAnimationFrame to avoid conflicts with Owl's rendering cycle
            requestAnimationFrame(async () => {
                try {
                    if (this.messageState?.isDestroyed || !this.tableRef?.el) {
                        return;
                    }

                    await this.props.list.model.load();

                    // Check again after async operation
                    if (this.messageState?.isDestroyed || !this.tableRef?.el) {
                        return;
                    }

                    // Let Owl handle the re-rendering instead of manual DOM manipulation
                    this.messageState.needsRefresh = true;
                    this.props.list.model.notify();

                    // Schedule safe rendering after Owl's patch cycle
                    setTimeout(() => {
                        if (!this.messageState?.isDestroyed && this.tableRef?.el) {
                            this.renderMailIconsSafely();
                        }
                    }, 0);
                } catch (innerError) {
                    // Silently handle any nested errors during the update
                    console.debug("Inner error during message update:", innerError);
                }
            });
        } catch (error) {
            // Silently handle component destruction errors
            if (error.message && (
                error.message.includes('destroyed') ||
                error.message.includes('Component is destroyed') ||
                error.message.includes('node') ||
                error.message.includes('insertBefore')
            )) {
                return;
            }
            console.error("Error updating message content:", error);
        }
    }

    setupFilterButtonsSafely() {
        // Enhanced safety checks to prevent DOM manipulation during Owl lifecycle
        if (this.messageState?.isDestroyed ||
            !this.tableRef?.el?.parentElement?.parentElement?.parentElement ||
            this.tableRef.el.parentElement.parentElement.parentElement.querySelectorAll('div.btn-group').length > 0) {
            return;
        }

        try {
            const buttonContainer = document.createElement('div');
            buttonContainer.className = 'btn-group';
            buttonContainer.style.padding = '10px 0px 0px 0px';

            Object.entries(this.filterButtons).forEach(([type, config]) => {
                const button = document.createElement('button');
                button.className = 'btn btn-secondary filter-custom';

                const icon = document.createElement('i');
                icon.className = `fa ${config.icon}`;
                button.appendChild(icon);

                button.addEventListener('click', () => {
                    if (!this.messageState?.isDestroyed) {
                        this.onClickFilter(type);
                    }
                });
                buttonContainer.appendChild(button);
            });

            // Double-check before DOM insertion
            if (!this.messageState?.isDestroyed && this.tableRef?.el?.parentElement?.parentElement?.parentElement) {
                this.tableRef.el.parentElement.parentElement.parentElement.prepend(buttonContainer);
            }
        } catch (error) {
            // Silently handle DOM manipulation errors during component destruction
            console.debug('Could not add filter buttons - component may be destroyed:', error);
        }
    }

    renderMailIconsSafely() {
        // Enhanced safety checks to prevent DOM manipulation errors during Owl lifecycle
        if (this.messageState?.isDestroyed ||
            !this.tableRef?.el ||
            !this.tableRef.el.parentElement ||
            !this.props?.list?.records) {
            return;
        }

        try {
            // Use CSS classes and data attributes instead of direct DOM manipulation
            this.tableRef.el.querySelectorAll('th').forEach((header) => {
                if (this.messageState?.isDestroyed) return;

                const dataName = header.getAttribute('data-name');
                if (dataName === 'message_type_mail') {
                    header.classList.add('o_message_type_header_hidden');
                }
                if (this.props.list.resModel === "mail.message"
                    && this.props.list.model.root.resModel === "helpdesk.ticket"
                    && dataName === 'body'
                ) {
                    header.classList.add('o_message_body_header');
                }
            });

            this.tableRef.el.querySelectorAll('td.o_data_cell').forEach((cellEl) => {
                if (this.messageState?.isDestroyed) return;

                const cellName = cellEl.getAttribute('name');
                const cellId = cellEl.parentNode?.getAttribute("data-id");
                const record = this.props.list.records.find(record => record.id === cellId);

                if (!record || !record.data) {
                    return;
                }

                // Handle empty body records by adding CSS class instead of hiding
                if (!record.data.body || !record.data.body.toString()) {
                    cellEl.parentElement?.classList.add('o_message_empty_body');
                    return;
                }

                if (cellName === 'message_type_mail' && !cellEl.querySelector('.o_message_type_icon')) {
                    const email_from = record.data['email_from'] || '';
                    const message_type_mail = record.data['message_type_mail'];
                    let iconClass = '';
                    let title = '';

                    switch (message_type_mail) {
                        case 'email_sent':
                            iconClass = 'fa fa-long-arrow-left color-red';
                            title = `To: ${email_from}`;
                            break;
                        case 'email_received':
                            iconClass = 'fa fa-long-arrow-right color-black';
                            title = `From: ${email_from}`;
                            break;
                        case 'note':
                            iconClass = 'fa fa-file-text-o color-green';
                            title = `User: ${email_from}`;
                            break;
                    }

                    if (iconClass) {
                        const icon = document.createElement('i');
                        icon.className = `${iconClass} o_message_type_icon`;
                        icon.title = title;

                        // Safely replace content only if cell is empty or needs update
                        if (cellEl.children.length === 0 || !cellEl.querySelector('.o_message_type_icon')) {
                            cellEl.innerHTML = '';
                            cellEl.appendChild(icon);
                        }
                    }
                }
            });
        } catch (error) {
            // Silently handle any DOM manipulation errors
            console.debug('Error during safe mail icon rendering:', error);
        }
    }

    onClickFilter(selectedType) {
        Object.entries(this.filterButtons).forEach(([type, config]) => {
            if (type !== selectedType && config.active) {
                this.toggleFilter(type);
            }
        });

        this.toggleFilter(selectedType);
    }

    toggleFilter(type) {
        const rows = this.tableRef.el.querySelectorAll('tr.o_data_row');
        const button = this.tableRef.el.parentElement.parentElement.parentElement.parentElement.querySelector(`.filter-custom i.${this.filterButtons[type].icon.replaceAll(" ", ".")}`).parentElement;
        const isActive = this.filterButtons[type].active;

        rows.forEach(row => {
            const icon = row.querySelector('td:first-child i');
            const shouldHide = icon && !icon.classList.value.includes(this.filterButtons[type].icon);

            if (shouldHide && !isActive) {
                row.style.display = 'none';
                button.style.backgroundColor = '#7C7BAD';
            } else if (shouldHide && isActive) {
                row.style.display = '';
                button.style.removeProperty('background-color');
            }
        });

        this.filterButtons[type].active = !isActive;
    }

    getCellClass(column, record) {
        let classes = super.getCellClass(column, record);
        if (column.name === 'message_type_mail') {
            classes += ' text-center';
        }
        return classes;
    }

    async onCellClicked(record, column, ev) {
        if (this.props.list.model.root.resModel === "helpdesk.ticket"
            && this.props.list.resModel === "mail.message"
            // TODO: We need something like below to be more precise
            // && ev.target.closest('.o_field_list_mail_icon_one2many')
        ) {
            // Add safety checks to prevent errors during component destruction
            if (!this.tableRef?.el || this.__isDestroyed) {
                return;
            }

            try {
                this.tableRef.el.querySelectorAll('td.o_data_cell').forEach(async (cellEl) => {
                    if (!this.tableRef?.el || this.__isDestroyed) return;

                    if (cellEl.parentNode.getAttribute("data-id") !== record.id) return;
                    if (record.data.scheduled_date) {
                        const action = await this.orm.call(
                            record.resModel, MESSAGE_TYPE_MAIL_ACTION_MAP['email_scheduled'], [record.data.id], {}
                        );
                        if (action && !this.__isDestroyed) {
                            this.action.doAction(action);
                            return;
                        }
                    }
                    const action_name = MESSAGE_TYPE_MAIL_ACTION_MAP[record.data.message_type_mail];
                    if (!action_name) {
                        console.warn(`No action mapped for message type ${record.data.message_type_mail}`);
                        return;
                    }
                    const action = await this.orm.call(
                        record.resModel, action_name, [record.data.id], {}
                    );
                    if (action && !this.__isDestroyed) {
                        this.action.doAction(action);
                        return;
                    }
                });
                return;
            } catch (error) {
                // Silently handle component destruction errors
                console.debug('Error in cell click handler:', error);
            }
        }
        return await this._super(record, column, ev);
    }
}

export class MailIconX2ManyField extends X2ManyField {
    setup() {
        super.setup();
    }
}

MailIconX2ManyField.components = {
    ...X2ManyField.components,
    ListRenderer: ListRendererMailIcon,
};

registry.category("fields").add("list_mail_icon_one2many", MailIconX2ManyField);
