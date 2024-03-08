#---------------------------------------------------------------#
#    purpose : create a ticket in each location                 #
#    source:                                                    #
#    output :                                                   #
#---------------------------------------------------------------#

info_widget("", "1. Request a CASTR self service template, a configuration file change, or anything related to CASTR","success")
link_widget(ticket_management.sim_link_castr.value,"")
info_widget("", "2. Report an issue related to WALLE, or request a small automation project help","success")
link_widget(ticket_management.sim_link_walle.value,"")