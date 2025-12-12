.. tab-set::

    .. tab-item:: components

        .. container:: accordion-group

            .. dropdown:: Component
                
                Class documentation and example: :py:class:`Component <tespy.components.component.Component>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
        
        

    .. tab-item:: basics

        .. container:: accordion-group

            .. dropdown:: CycleCloser
                
                Class documentation and example: :py:class:`CycleCloser <tespy.components.basics.cycle_closer.CycleCloser>`
                
                Table of constraints
                
                ============================  ============================  =======================================================================================================================
                Parameter                     Description                   Method
                ============================  ============================  =======================================================================================================================
                pressure_equality_constraint  pressure equality constraint  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                enthalpy_equality_constraint  enthalpy equality constraint  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                ============================  ============================  =======================================================================================================================
                
                Table of parameters
                
                ===============  ========================================================================  ============  ============
                Parameter        Description                                                               Quantity      Method
                ===============  ========================================================================  ============  ============
                mass_deviation   absolute deviation of mass flow between inlet and outlet                  mass_flow     :code:`None`
                fluid_deviation  norm of absolute deviation of fluid composition between inlet and outlet  :code:`None`  :code:`None`
                ===============  ========================================================================  ============  ============
        
        


            .. dropdown:: Sink
                
                Class documentation and example: :py:class:`Sink <tespy.components.basics.sink.Sink>`
        
        


            .. dropdown:: Source
                
                Class documentation and example: :py:class:`Source <tespy.components.basics.source.Source>`
        
        


            .. dropdown:: SubsystemInterface
                
                Class documentation and example: :py:class:`SubsystemInterface <tespy.components.basics.subsystem_interface.SubsystemInterface>`
                
                Table of constraints
                
                ============================  ========================================  =======================================================================================================================
                Parameter                     Description                               Method
                ============================  ========================================  =======================================================================================================================
                mass_flow_constraints         mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints             fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                pressure_equality_constraint  pressure equality constraint              :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                enthalpy_equality_constraint  enthalpy equality constraint              :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                ============================  ========================================  =======================================================================================================================
                
                Table of parameters
                
                ===========  =================================  ============  ============
                Parameter    Description                        Quantity      Method
                ===========  =================================  ============  ============
                num_inter    number of interfacing connections  :code:`None`  :code:`None`
                ===========  =================================  ============  ============
        
        

    .. tab-item:: combustion

        .. container:: accordion-group

            .. dropdown:: CombustionChamber
                
                Class documentation and example: :py:class:`CombustionChamber <tespy.components.combustion.base.CombustionChamber>`
                
                Table of constraints
                
                ============================  ===============================================  =========================================================================================================================================
                Parameter                     Description                                      Method
                ============================  ===============================================  =========================================================================================================================================
                mass_flow_constraints         mass flow balance over all inflows and outflows  :py:meth:`mass_flow_func <tespy.components.combustion.base.CombustionChamber.mass_flow_func>`
                reactor_pressure_constraints  pressure equality constraints                    :py:meth:`combustion_pressure_structure_matrix <tespy.components.combustion.base.CombustionChamber.combustion_pressure_structure_matrix>`
                stoichiometry_constraints     constraints for stoichiometry of the reaction    :py:meth:`stoichiometry_func <tespy.components.combustion.base.CombustionChamber.stoichiometry_func>`
                energy_balance_constraints    constraint for energy balance                    :py:meth:`energy_balance_func <tespy.components.combustion.base.CombustionChamber.energy_balance_func>`
                ============================  ===============================================  =========================================================================================================================================
                
                Table of parameters
                
                ===========  ==================================================  ==========  =======================================================================================
                Parameter    Description                                         Quantity    Method
                ===========  ==================================================  ==========  =======================================================================================
                lamb         available oxygen to stoichiometric oxygen ratio     ratio       :py:meth:`lambda_func <tespy.components.combustion.base.CombustionChamber.lambda_func>`
                ti           thermal input (fuel LHV multiplied with mass flow)  heat        :py:meth:`ti_func <tespy.components.combustion.base.CombustionChamber.ti_func>`
                ===========  ==================================================  ==========  =======================================================================================
        
        


            .. dropdown:: DiabaticCombustionChamber
                
                Class documentation and example: :py:class:`DiabaticCombustionChamber <tespy.components.combustion.diabatic.DiabaticCombustionChamber>`
                
                Table of constraints
                
                =========================  ===============================================  =====================================================================================================
                Parameter                  Description                                      Method
                =========================  ===============================================  =====================================================================================================
                mass_flow_constraints      mass flow balance over all inflows and outflows  :py:meth:`mass_flow_func <tespy.components.combustion.base.CombustionChamber.mass_flow_func>`
                stoichiometry_constraints  constraints for stoichiometry of the reaction    :py:meth:`stoichiometry_func <tespy.components.combustion.base.CombustionChamber.stoichiometry_func>`
                =========================  ===============================================  =====================================================================================================
                
                Table of parameters
                
                ===========  ==================================================  ==========  ===================================================================================================================
                Parameter    Description                                         Quantity    Method
                ===========  ==================================================  ==========  ===================================================================================================================
                lamb         available oxygen to stoichiometric oxygen ratio     ratio       :py:meth:`lambda_func <tespy.components.combustion.base.CombustionChamber.lambda_func>`
                ti           thermal input (fuel LHV multiplied with mass flow)  heat        :py:meth:`ti_func <tespy.components.combustion.base.CombustionChamber.ti_func>`
                pr           outlet 0 to inlet 0 pressure ratio                  ratio       :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp           inlet 0 to outlet 0 absolute pressure change        pressure    :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                eta          heat dissipation ratio relative to thermal input    efficiency  :py:meth:`energy_balance_func <tespy.components.combustion.diabatic.DiabaticCombustionChamber.energy_balance_func>`
                Qloss        heat dissipation                                    heat        :code:`None`
                ===========  ==================================================  ==========  ===================================================================================================================
        
        


            .. dropdown:: CombustionEngine
                
                Class documentation and example: :py:class:`CombustionEngine <tespy.components.combustion.engine.CombustionEngine>`
                
                Table of constraints
                
                =============================  =====================================================================  =========================================================================================================================================
                Parameter                      Description                                                            Method
                =============================  =====================================================================  =========================================================================================================================================
                mass_flow_constraints          mass flow balance over all inflows and outflows                        :py:meth:`mass_flow_func <tespy.components.combustion.base.CombustionChamber.mass_flow_func>`
                reactor_pressure_constraints   pressure equality constraints                                          :py:meth:`combustion_pressure_structure_matrix <tespy.components.combustion.base.CombustionChamber.combustion_pressure_structure_matrix>`
                stoichiometry_constraints      constraints for stoichiometry of the reaction                          :py:meth:`stoichiometry_func <tespy.components.combustion.base.CombustionChamber.stoichiometry_func>`
                energy_balance_constraints     constraint for energy balance                                          :py:meth:`energy_balance_func <tespy.components.combustion.engine.CombustionEngine.energy_balance_func>`
                power_constraints              equation for thermal input to power generation relation                :py:meth:`tiP_char_func <tespy.components.combustion.engine.CombustionEngine.tiP_char_func>`
                heat1_constraints              equation for thermal input to heating port 1 heat generation relation  :py:meth:`Q1_char_func <tespy.components.combustion.engine.CombustionEngine.Q1_char_func>`
                heat2_constraints              equation for thermal input to heating port 2 heat generation relation  :py:meth:`Q2_char_func <tespy.components.combustion.engine.CombustionEngine.Q2_char_func>`
                heatloss_constraints           equation for thermal input to heat dissipation relation                :py:meth:`Qloss_char_func <tespy.components.combustion.engine.CombustionEngine.Qloss_char_func>`
                mass_flow_cooling_constraints  equation for mass flow equality at heating ports                       :py:meth:`variable_equality_structure_matrix <tespy.components.combustion.engine.CombustionEngine.variable_equality_structure_matrix>`
                fluid_cooling_constraints      equation for fluid composition equality at heating ports               :py:meth:`variable_equality_structure_matrix <tespy.components.combustion.engine.CombustionEngine.variable_equality_structure_matrix>`
                =============================  =====================================================================  =========================================================================================================================================
                
                Table of parameters
                
                ===========  =================================================================================  ============  =========================================================================================
                Parameter    Description                                                                        Quantity      Method
                ===========  =================================================================================  ============  =========================================================================================
                lamb         available oxygen to stoichiometric oxygen ratio                                    ratio         :py:meth:`lambda_func <tespy.components.combustion.base.CombustionChamber.lambda_func>`
                ti           thermal input (fuel LHV multiplied with mass flow)                                 heat          :py:meth:`ti_func <tespy.components.combustion.base.CombustionChamber.ti_func>`
                P [1]_       mechanical power generated by the engine                                           power         :code:`None`
                Q1           heating port 1 heat production                                                     heat          :py:meth:`Q1_func <tespy.components.combustion.engine.CombustionEngine.Q1_func>`
                Q2           heating port 2 heat production                                                     heat          :py:meth:`Q2_func <tespy.components.combustion.engine.CombustionEngine.Q2_func>`
                Qloss [1]_   heat dissipation                                                                   heat          :code:`None`
                pr1          heating port 1 outlet to inlet pressure ratio                                      ratio         :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                pr2          heating port 2 outlet to inlet pressure ratio                                      ratio         :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp1          heating port 1 inlet to outlet absolute pressure change                            pressure      :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                dp2          heating port 2 inlet to outlet absolute pressure change                            pressure      :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                zeta1        heating port 1 non-dimensional friction coefficient for pressure loss calculation  :code:`None`  :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                zeta2        heating port 2 non-dimensional friction coefficient for pressure loss calculation  :code:`None`  :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                eta_mech     :code:`None`                                                                       :code:`None`  :code:`None`
                T_v_inner    :code:`None`                                                                       :code:`None`  :code:`None`
                ===========  =================================================================================  ============  =========================================================================================
                
                Table of characteristic lines and maps
                
                ===========  =======================================================  ============
                Parameter    Description                                              Method
                ===========  =======================================================  ============
                tiP_char     thermal input to power lookup table                      :code:`None`
                Q1_char      thermal input to heat production of port 1 lookup table  :code:`None`
                Q2_char      thermal input to heat production of port 2 lookup table  :code:`None`
                Qloss_char   thermal input to heat dissipation lookup table           :code:`None`
                ===========  =======================================================  ============
        
        

    .. tab-item:: displacementmachinery

        .. container:: accordion-group

            .. dropdown:: DisplacementMachine
                
                Class documentation and example: :py:class:`DisplacementMachine <tespy.components.displacementmachinery.base.DisplacementMachine>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
                
                Table of parameters
                
                ===========  ========================================  ==========  ====================================================================================================================
                Parameter    Description                               Quantity    Method
                ===========  ========================================  ==========  ====================================================================================================================
                P            power input of the component              power       :py:meth:`energy_balance_func <tespy.components.displacementmachinery.base.DisplacementMachine.energy_balance_func>`
                pr           outlet to inlet pressure ratio            ratio       :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp           inlet to outlet absolute pressure change  pressure    :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                ===========  ========================================  ==========  ====================================================================================================================
        
        


            .. dropdown:: PolynomialCompressor
                
                Class documentation and example: :py:class:`PolynomialCompressor <tespy.components.displacementmachinery.polynomial_compressor.PolynomialCompressor>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
                
                Table of parameters
                
                =================  ==============================================================================  ============  =========================================================================================
                Parameter          Description                                                                     Quantity      Method
                =================  ==============================================================================  ============  =========================================================================================
                P                  power consumption                                                               power         :code:`None`
                pr                 outlet to inlet pressure ratio                                                  ratio         :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp                 inlet to outlet absolute pressure change                                        pressure      :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                Q_diss             heat dissipation                                                                heat          :code:`None`
                eta_vol            volumetric efficiency                                                           efficiency    :code:`None`
                dissipation_ratio  heat dissipation ratio relative to power consumption                            ratio         :code:`None`
                Q_diss_rel         heat dissipation ratio relative to power consumption(deprecated)                ratio         :code:`None`
                rpm [1]_           compressor frequency                                                            :code:`None`  :code:`None`
                reference_state    reference state definition for the scaling of displacement with compressor rpm  :code:`None`  :code:`None`
                eta_s_poly         polynomial coefficients for isentropic efficiency                               :code:`None`  :code:`None`
                eta_vol_poly       polynomial coefficients for volumetric efficiency                               :code:`None`  :code:`None`
                eta_s              isentropic efficiency                                                           efficiency    :code:`None`
                =================  ==============================================================================  ============  =========================================================================================
                
                Table of parameter groups
                
                ====================  ================================================================================  ==========================================================  ==================================================================================================================================================
                Parameter             Description                                                                       Required parameters                                         Method
                ====================  ================================================================================  ==========================================================  ==================================================================================================================================================
                eta_vol_poly_group    displacement equation based on polynomial coefficients for volumetric efficiency  :code:`reference_state`, :code:`eta_vol_poly`, :code:`rpm`  :py:meth:`eta_vol_poly_group_func <tespy.components.displacementmachinery.polynomial_compressor.PolynomialCompressor.eta_vol_poly_group_func>`
                eta_vol_group         displacement equation based on fixed volumetric efficiency                        :code:`reference_state`, :code:`eta_vol`, :code:`rpm`       :py:meth:`eta_vol_group_func <tespy.components.displacementmachinery.polynomial_compressor.PolynomialCompressor.eta_vol_group_func>`
                eta_s_poly_group      isentropic efficiency equation based on polynomial coefficients                   :code:`eta_s_poly`, :code:`dissipation_ratio`               :py:meth:`eta_s_poly_group_func <tespy.components.displacementmachinery.polynomial_compressor.PolynomialCompressor.eta_s_poly_group_func>`
                eta_s_group           isentropic efficiency equation with fixed efficiency                              :code:`eta_s`, :code:`dissipation_ratio`                    :py:meth:`eta_s_group_func <tespy.components.displacementmachinery.polynomial_compressor.PolynomialCompressor.eta_s_group_func>`
                energy_balance_group  energy balance equation for fixed power and dissipation ratio                     :code:`P`, :code:`dissipation_ratio`                        :py:meth:`energy_balance_group_func <tespy.components.displacementmachinery.polynomial_compressor.PolynomialCompressor.energy_balance_group_func>`
                ====================  ================================================================================  ==========================================================  ==================================================================================================================================================
        
        


            .. dropdown:: PolynomialCompressorWithCooling
                
                Class documentation and example: :py:class:`PolynomialCompressorWithCooling <tespy.components.displacementmachinery.polynomial_compressor_with_cooling.PolynomialCompressorWithCooling>`
                
                Table of constraints
                
                ==================================  ========================================  ==============================================================================================================================================================================
                Parameter                           Description                               Method
                ==================================  ========================================  ==============================================================================================================================================================================
                mass_flow_constraints               mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints                   fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                cooling_energy_balance_constraints  energy balance for the cooling ports      :py:meth:`cooling_energy_balance_func <tespy.components.displacementmachinery.polynomial_compressor_with_cooling.PolynomialCompressorWithCooling.cooling_energy_balance_func>`
                ==================================  ========================================  ==============================================================================================================================================================================
                
                Table of parameters
                
                =================  ==============================================================================  ======================  =========================================================================================
                Parameter          Description                                                                     Quantity                Method
                =================  ==============================================================================  ======================  =========================================================================================
                P                  power consumption                                                               power                   :code:`None`
                pr                 outlet to inlet pressure ratio                                                  ratio                   :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp                 inlet to outlet absolute pressure change                                        pressure                :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                Q_diss             heat dissipation                                                                heat                    :code:`None`
                eta_vol            volumetric efficiency                                                           efficiency              :code:`None`
                dissipation_ratio  heat dissipation ratio relative to power consumption                            ratio                   :code:`None`
                Q_diss_rel         heat dissipation ratio relative to power consumption(deprecated)                ratio                   :code:`None`
                rpm [1]_           compressor frequency                                                            :code:`None`            :code:`None`
                reference_state    reference state definition for the scaling of displacement with compressor rpm  :code:`None`            :code:`None`
                eta_s_poly         polynomial coefficients for isentropic efficiency                               :code:`None`            :code:`None`
                eta_vol_poly       polynomial coefficients for volumetric efficiency                               :code:`None`            :code:`None`
                eta_s              isentropic efficiency                                                           efficiency              :code:`None`
                eta_recovery       share of dissipated heat usable in cooling port                                 efficiency              :code:`None`
                td_minimal         theoretical minimal temperature difference between working and cooling fluid    temperature_difference  :code:`None`
                dp_cooling         cooling port inlet to outlet absolute pressure change                           pressure                :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                pr_cooling         cooling port outlet to inlet pressure ratio                                     ratio                   :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                =================  ==============================================================================  ======================  =========================================================================================
                
                Table of parameter groups
                
                ====================  ================================================================================  ==========================================================  ==================================================================================================================================================
                Parameter             Description                                                                       Required parameters                                         Method
                ====================  ================================================================================  ==========================================================  ==================================================================================================================================================
                eta_vol_poly_group    displacement equation based on polynomial coefficients for volumetric efficiency  :code:`reference_state`, :code:`eta_vol_poly`, :code:`rpm`  :py:meth:`eta_vol_poly_group_func <tespy.components.displacementmachinery.polynomial_compressor.PolynomialCompressor.eta_vol_poly_group_func>`
                eta_vol_group         displacement equation based on fixed volumetric efficiency                        :code:`reference_state`, :code:`eta_vol`, :code:`rpm`       :py:meth:`eta_vol_group_func <tespy.components.displacementmachinery.polynomial_compressor.PolynomialCompressor.eta_vol_group_func>`
                eta_s_poly_group      isentropic efficiency equation based on polynomial coefficients                   :code:`eta_s_poly`, :code:`dissipation_ratio`               :py:meth:`eta_s_poly_group_func <tespy.components.displacementmachinery.polynomial_compressor.PolynomialCompressor.eta_s_poly_group_func>`
                eta_s_group           isentropic efficiency equation with fixed efficiency                              :code:`eta_s`, :code:`dissipation_ratio`                    :py:meth:`eta_s_group_func <tespy.components.displacementmachinery.polynomial_compressor.PolynomialCompressor.eta_s_group_func>`
                energy_balance_group  energy balance equation for fixed power and dissipation ratio                     :code:`P`, :code:`dissipation_ratio`                        :py:meth:`energy_balance_group_func <tespy.components.displacementmachinery.polynomial_compressor.PolynomialCompressor.energy_balance_group_func>`
                ====================  ================================================================================  ==========================================================  ==================================================================================================================================================
        
        

    .. tab-item:: heat_exchangers

        .. container:: accordion-group

            .. dropdown:: HeatExchanger
                
                Class documentation and example: :py:class:`HeatExchanger <tespy.components.heat_exchangers.base.HeatExchanger>`
                
                Table of constraints
                
                ==========================  ============================================  =======================================================================================================================
                Parameter                   Description                                   Method
                ==========================  ============================================  =======================================================================================================================
                mass_flow_constraints       mass flow equality constraint(s)              :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints           fluid composition equality constraint(s)      :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                energy_balance_constraints  hot side to cold side heat transfer equation  :py:meth:`energy_balance_func <tespy.components.heat_exchangers.base.HeatExchanger.energy_balance_func>`
                ==========================  ============================================  =======================================================================================================================
                
                Table of parameters
                
                ===========  ============================================================================  =========================  ================================================================================================================
                Parameter    Description                                                                   Quantity                   Method
                ===========  ============================================================================  =========================  ================================================================================================================
                Q            heat transfer from hot side                                                   heat                       :py:meth:`energy_balance_hot_func <tespy.components.heat_exchangers.base.HeatExchanger.energy_balance_hot_func>`
                kA           heat transfer coefficient considering terminal temperature differences        heat_transfer_coefficient  :py:meth:`kA_func <tespy.components.heat_exchangers.base.HeatExchanger.kA_func>`
                td_log       logarithmic temperature difference                                            temperature_difference     :code:`None`
                ttd_u        terminal temperature difference at hot side inlet to cold side outlet         temperature_difference     :py:meth:`ttd_u_func <tespy.components.heat_exchangers.base.HeatExchanger.ttd_u_func>`
                ttd_l        terminal temperature difference at hot side outlet to cold side inlet         temperature_difference     :py:meth:`ttd_l_func <tespy.components.heat_exchangers.base.HeatExchanger.ttd_l_func>`
                ttd_min      minimum terminal temperature difference                                       temperature_difference     :py:meth:`ttd_min_func <tespy.components.heat_exchangers.base.HeatExchanger.ttd_min_func>`
                pr1          hot side outlet to inlet pressure ratio                                       ratio                      :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                pr2          cold side outlet to inlet pressure ratio                                      ratio                      :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp1          hot side inlet to outlet absolute pressure change                             pressure                   :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                dp2          cold side inlet to outlet absolute pressure change                            pressure                   :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                zeta1        hot side non-dimensional friction coefficient for pressure loss calculation   :code:`None`               :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                zeta2        cold side non-dimensional friction coefficient for pressure loss calculation  :code:`None`               :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                eff_cold     heat exchanger effectiveness for cold side                                    efficiency                 :py:meth:`eff_cold_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_cold_func>`
                eff_hot      heat exchanger effectiveness for hot side                                     efficiency                 :py:meth:`eff_hot_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_hot_func>`
                eff_max      maximum heat exchanger effectiveness                                          efficiency                 :py:meth:`eff_max_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_max_func>`
                ===========  ============================================================================  =========================  ================================================================================================================
                
                Table of parameter groups
                
                ===========  ==============================================================  ==================================  ==========================================================================================
                Parameter    Description                                                     Required parameters                 Method
                ===========  ==============================================================  ==================================  ==========================================================================================
                kA_char      equation for heat transfer based on kA and modification factor  :code:`kA_char1`, :code:`kA_char2`  :py:meth:`kA_char_func <tespy.components.heat_exchangers.base.HeatExchanger.kA_char_func>`
                ===========  ==============================================================  ==================================  ==========================================================================================
                
                Table of characteristic lines and maps
                
                ===========  ====================================================  ============
                Parameter    Description                                           Method
                ===========  ====================================================  ============
                kA_char1     hot side kA modification lookup table for offdesign   :code:`None`
                kA_char2     cold side kA modification lookup table for offdesign  :code:`None`
                ===========  ====================================================  ============
        
        


            .. dropdown:: Condenser
                
                Class documentation and example: :py:class:`Condenser <tespy.components.heat_exchangers.condenser.Condenser>`
                
                Table of constraints
                
                ==========================  ============================================  =======================================================================================================================
                Parameter                   Description                                   Method
                ==========================  ============================================  =======================================================================================================================
                mass_flow_constraints       mass flow equality constraint(s)              :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints           fluid composition equality constraint(s)      :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                energy_balance_constraints  hot side to cold side heat transfer equation  :py:meth:`energy_balance_func <tespy.components.heat_exchangers.base.HeatExchanger.energy_balance_func>`
                ==========================  ============================================  =======================================================================================================================
                
                Table of parameters
                
                ===========  ============================================================================  =========================  ================================================================================================================
                Parameter    Description                                                                   Quantity                   Method
                ===========  ============================================================================  =========================  ================================================================================================================
                Q            heat transfer from hot side                                                   heat                       :py:meth:`energy_balance_hot_func <tespy.components.heat_exchangers.base.HeatExchanger.energy_balance_hot_func>`
                kA           heat transfer coefficient considering terminal temperature differences        heat_transfer_coefficient  :py:meth:`kA_func <tespy.components.heat_exchangers.base.HeatExchanger.kA_func>`
                td_log       logarithmic temperature difference                                            temperature_difference     :code:`None`
                ttd_u        terminal temperature difference at hot side inlet to cold side outlet         temperature_difference     :py:meth:`ttd_u_func <tespy.components.heat_exchangers.condenser.Condenser.ttd_u_func>`
                ttd_l        terminal temperature difference at hot side outlet to cold side inlet         temperature_difference     :py:meth:`ttd_l_func <tespy.components.heat_exchangers.base.HeatExchanger.ttd_l_func>`
                ttd_min      minimum terminal temperature difference                                       temperature_difference     :py:meth:`ttd_min_func <tespy.components.heat_exchangers.base.HeatExchanger.ttd_min_func>`
                pr1          hot side outlet to inlet pressure ratio                                       ratio                      :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                pr2          cold side outlet to inlet pressure ratio                                      ratio                      :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp1          hot side inlet to outlet absolute pressure change                             pressure                   :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                dp2          cold side inlet to outlet absolute pressure change                            pressure                   :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                zeta1        hot side non-dimensional friction coefficient for pressure loss calculation   :code:`None`               :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                zeta2        cold side non-dimensional friction coefficient for pressure loss calculation  :code:`None`               :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                eff_cold     heat exchanger effectiveness for cold side                                    efficiency                 :py:meth:`eff_cold_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_cold_func>`
                eff_hot      heat exchanger effectiveness for hot side                                     efficiency                 :py:meth:`eff_hot_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_hot_func>`
                eff_max      maximum heat exchanger effectiveness                                          efficiency                 :py:meth:`eff_max_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_max_func>`
                subcooling   allow subcooling in the condenser                                             :code:`None`               :py:meth:`subcooling_func <tespy.components.heat_exchangers.condenser.Condenser.subcooling_func>`
                ===========  ============================================================================  =========================  ================================================================================================================
                
                Table of parameter groups
                
                ===========  ==============================================================  ==================================  ===========================================================================================
                Parameter    Description                                                     Required parameters                 Method
                ===========  ==============================================================  ==================================  ===========================================================================================
                kA_char      equation for heat transfer based on kA and modification factor  :code:`kA_char1`, :code:`kA_char2`  :py:meth:`kA_char_func <tespy.components.heat_exchangers.condenser.Condenser.kA_char_func>`
                ===========  ==============================================================  ==================================  ===========================================================================================
                
                Table of characteristic lines and maps
                
                ===========  ====================================================  ============
                Parameter    Description                                           Method
                ===========  ====================================================  ============
                kA_char1     hot side kA modification lookup table for offdesign   :code:`None`
                kA_char2     cold side kA modification lookup table for offdesign  :code:`None`
                ===========  ====================================================  ============
        
        


            .. dropdown:: Desuperheater
                
                Class documentation and example: :py:class:`Desuperheater <tespy.components.heat_exchangers.desuperheater.Desuperheater>`
                
                Table of constraints
                
                ==========================  =============================================  =======================================================================================================================
                Parameter                   Description                                    Method
                ==========================  =============================================  =======================================================================================================================
                mass_flow_constraints       mass flow equality constraint(s)               :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints           fluid composition equality constraint(s)       :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                energy_balance_constraints  hot side to cold side heat transfer equation   :py:meth:`energy_balance_func <tespy.components.heat_exchangers.base.HeatExchanger.energy_balance_func>`
                saturated_gas_constraints   equation for saturated gas at hot side outlet  :py:meth:`saturated_gas_func <tespy.components.heat_exchangers.desuperheater.Desuperheater.saturated_gas_func>`
                ==========================  =============================================  =======================================================================================================================
                
                Table of parameters
                
                ===========  ============================================================================  =========================  ================================================================================================================
                Parameter    Description                                                                   Quantity                   Method
                ===========  ============================================================================  =========================  ================================================================================================================
                Q            heat transfer from hot side                                                   heat                       :py:meth:`energy_balance_hot_func <tespy.components.heat_exchangers.base.HeatExchanger.energy_balance_hot_func>`
                kA           heat transfer coefficient considering terminal temperature differences        heat_transfer_coefficient  :py:meth:`kA_func <tespy.components.heat_exchangers.base.HeatExchanger.kA_func>`
                td_log       logarithmic temperature difference                                            temperature_difference     :code:`None`
                ttd_u        terminal temperature difference at hot side inlet to cold side outlet         temperature_difference     :py:meth:`ttd_u_func <tespy.components.heat_exchangers.base.HeatExchanger.ttd_u_func>`
                ttd_l        terminal temperature difference at hot side outlet to cold side inlet         temperature_difference     :py:meth:`ttd_l_func <tespy.components.heat_exchangers.base.HeatExchanger.ttd_l_func>`
                ttd_min      minimum terminal temperature difference                                       temperature_difference     :py:meth:`ttd_min_func <tespy.components.heat_exchangers.base.HeatExchanger.ttd_min_func>`
                pr1          hot side outlet to inlet pressure ratio                                       ratio                      :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                pr2          cold side outlet to inlet pressure ratio                                      ratio                      :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp1          hot side inlet to outlet absolute pressure change                             pressure                   :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                dp2          cold side inlet to outlet absolute pressure change                            pressure                   :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                zeta1        hot side non-dimensional friction coefficient for pressure loss calculation   :code:`None`               :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                zeta2        cold side non-dimensional friction coefficient for pressure loss calculation  :code:`None`               :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                eff_cold     heat exchanger effectiveness for cold side                                    efficiency                 :py:meth:`eff_cold_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_cold_func>`
                eff_hot      heat exchanger effectiveness for hot side                                     efficiency                 :py:meth:`eff_hot_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_hot_func>`
                eff_max      maximum heat exchanger effectiveness                                          efficiency                 :py:meth:`eff_max_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_max_func>`
                ===========  ============================================================================  =========================  ================================================================================================================
                
                Table of parameter groups
                
                ===========  ==============================================================  ==================================  ==========================================================================================
                Parameter    Description                                                     Required parameters                 Method
                ===========  ==============================================================  ==================================  ==========================================================================================
                kA_char      equation for heat transfer based on kA and modification factor  :code:`kA_char1`, :code:`kA_char2`  :py:meth:`kA_char_func <tespy.components.heat_exchangers.base.HeatExchanger.kA_char_func>`
                ===========  ==============================================================  ==================================  ==========================================================================================
                
                Table of characteristic lines and maps
                
                ===========  ====================================================  ============
                Parameter    Description                                           Method
                ===========  ====================================================  ============
                kA_char1     hot side kA modification lookup table for offdesign   :code:`None`
                kA_char2     cold side kA modification lookup table for offdesign  :code:`None`
                ===========  ====================================================  ============
        
        


            .. dropdown:: SectionedHeatExchanger
                
                Class documentation and example: :py:class:`SectionedHeatExchanger <tespy.components.heat_exchangers.sectioned.SectionedHeatExchanger>`
                
                Table of constraints
                
                ==========================  ============================================  =======================================================================================================================
                Parameter                   Description                                   Method
                ==========================  ============================================  =======================================================================================================================
                mass_flow_constraints       mass flow equality constraint(s)              :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints           fluid composition equality constraint(s)      :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                energy_balance_constraints  hot side to cold side heat transfer equation  :py:meth:`energy_balance_func <tespy.components.heat_exchangers.base.HeatExchanger.energy_balance_func>`
                ==========================  ============================================  =======================================================================================================================
                
                Table of parameters
                
                =================  =============================================================================  =========================  ================================================================================================================
                Parameter          Description                                                                    Quantity                   Method
                =================  =============================================================================  =========================  ================================================================================================================
                Q                  heat transfer from hot side                                                    heat                       :py:meth:`energy_balance_hot_func <tespy.components.heat_exchangers.base.HeatExchanger.energy_balance_hot_func>`
                kA                 heat transfer coefficient considering terminal temperature differences         heat_transfer_coefficient  :py:meth:`kA_func <tespy.components.heat_exchangers.base.HeatExchanger.kA_func>`
                td_log             logarithmic temperature difference                                             temperature_difference     :code:`None`
                ttd_u              terminal temperature difference at hot side inlet to cold side outlet          temperature_difference     :py:meth:`ttd_u_func <tespy.components.heat_exchangers.base.HeatExchanger.ttd_u_func>`
                ttd_l              terminal temperature difference at hot side outlet to cold side inlet          temperature_difference     :py:meth:`ttd_l_func <tespy.components.heat_exchangers.base.HeatExchanger.ttd_l_func>`
                ttd_min            minimum terminal temperature difference                                        temperature_difference     :py:meth:`ttd_min_func <tespy.components.heat_exchangers.base.HeatExchanger.ttd_min_func>`
                pr1                hot side outlet to inlet pressure ratio                                        ratio                      :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                pr2                cold side outlet to inlet pressure ratio                                       ratio                      :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp1                hot side inlet to outlet absolute pressure change                              pressure                   :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                dp2                cold side inlet to outlet absolute pressure change                             pressure                   :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                zeta1              hot side non-dimensional friction coefficient for pressure loss calculation    :code:`None`               :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                zeta2              cold side non-dimensional friction coefficient for pressure loss calculation   :code:`None`               :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                eff_cold           heat exchanger effectiveness for cold side                                     efficiency                 :py:meth:`eff_cold_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_cold_func>`
                eff_hot            heat exchanger effectiveness for hot side                                      efficiency                 :py:meth:`eff_hot_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_hot_func>`
                eff_max            maximum heat exchanger effectiveness                                           efficiency                 :py:meth:`eff_max_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_max_func>`
                num_sections       number of sections of the heat exchanger                                       :code:`None`               :code:`None`
                UA                 sum of UA values of all sections of heat exchanger                             heat_transfer_coefficient  :py:meth:`UA_func <tespy.components.heat_exchangers.sectioned.SectionedHeatExchanger.UA_func>`
                refrigerant_index  side on which the refrigerant is flowing (0: hot, 1:cold)                      :code:`None`               :code:`None`
                re_exp_r           Reynolds exponent for UA modification based on refrigerant side mass flow      :code:`None`               :code:`None`
                re_exp_sf          Reynolds exponent for UA modification based on secondary fluid side mass flow  :code:`None`               :code:`None`
                alpha_ratio        secondary to refrigerant side convective heat transfer coefficient ratio       ratio                      :code:`None`
                area_ratio         secondary to refrigerant side heat transfer area ratio                         ratio                      :code:`None`
                td_pinch           equation for minimum pinch                                                     temperature_difference     :py:meth:`td_pinch_func <tespy.components.heat_exchangers.sectioned.SectionedHeatExchanger.td_pinch_func>`
                =================  =============================================================================  =========================  ================================================================================================================
                
                Table of parameter groups
                
                =============  ==============================================================  ============================================================================  ====================================================================================================================
                Parameter      Description                                                     Required parameters                                                           Method
                =============  ==============================================================  ============================================================================  ====================================================================================================================
                kA_char        equation for heat transfer based on kA and modification factor  :code:`kA_char1`, :code:`kA_char2`                                            :py:meth:`kA_char_func <tespy.components.heat_exchangers.base.HeatExchanger.kA_char_func>`
                UA_cecchinato  equation for UA modification in offdesign                       :code:`re_exp_r`, :code:`re_exp_sf`, :code:`alpha_ratio`, :code:`area_ratio`  :py:meth:`UA_cecchinato_func <tespy.components.heat_exchangers.sectioned.SectionedHeatExchanger.UA_cecchinato_func>`
                =============  ==============================================================  ============================================================================  ====================================================================================================================
                
                Table of characteristic lines and maps
                
                ===========  ====================================================  ============
                Parameter    Description                                           Method
                ===========  ====================================================  ============
                kA_char1     hot side kA modification lookup table for offdesign   :code:`None`
                kA_char2     cold side kA modification lookup table for offdesign  :code:`None`
                ===========  ====================================================  ============
        
        


            .. dropdown:: MovingBoundaryHeatExchanger
                
                Class documentation and example: :py:class:`MovingBoundaryHeatExchanger <tespy.components.heat_exchangers.movingboundary.MovingBoundaryHeatExchanger>`
                
                Table of constraints
                
                ==========================  ============================================  =======================================================================================================================
                Parameter                   Description                                   Method
                ==========================  ============================================  =======================================================================================================================
                mass_flow_constraints       mass flow equality constraint(s)              :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints           fluid composition equality constraint(s)      :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                energy_balance_constraints  hot side to cold side heat transfer equation  :py:meth:`energy_balance_func <tespy.components.heat_exchangers.base.HeatExchanger.energy_balance_func>`
                ==========================  ============================================  =======================================================================================================================
                
                Table of parameters
                
                =================  =============================================================================  =========================  ================================================================================================================
                Parameter          Description                                                                    Quantity                   Method
                =================  =============================================================================  =========================  ================================================================================================================
                Q                  heat transfer from hot side                                                    heat                       :py:meth:`energy_balance_hot_func <tespy.components.heat_exchangers.base.HeatExchanger.energy_balance_hot_func>`
                kA                 heat transfer coefficient considering terminal temperature differences         heat_transfer_coefficient  :py:meth:`kA_func <tespy.components.heat_exchangers.base.HeatExchanger.kA_func>`
                td_log             logarithmic temperature difference                                             temperature_difference     :code:`None`
                ttd_u              terminal temperature difference at hot side inlet to cold side outlet          temperature_difference     :py:meth:`ttd_u_func <tespy.components.heat_exchangers.base.HeatExchanger.ttd_u_func>`
                ttd_l              terminal temperature difference at hot side outlet to cold side inlet          temperature_difference     :py:meth:`ttd_l_func <tespy.components.heat_exchangers.base.HeatExchanger.ttd_l_func>`
                ttd_min            minimum terminal temperature difference                                        temperature_difference     :py:meth:`ttd_min_func <tespy.components.heat_exchangers.base.HeatExchanger.ttd_min_func>`
                pr1                hot side outlet to inlet pressure ratio                                        ratio                      :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                pr2                cold side outlet to inlet pressure ratio                                       ratio                      :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp1                hot side inlet to outlet absolute pressure change                              pressure                   :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                dp2                cold side inlet to outlet absolute pressure change                             pressure                   :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                zeta1              hot side non-dimensional friction coefficient for pressure loss calculation    :code:`None`               :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                zeta2              cold side non-dimensional friction coefficient for pressure loss calculation   :code:`None`               :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                eff_cold           heat exchanger effectiveness for cold side                                     efficiency                 :py:meth:`eff_cold_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_cold_func>`
                eff_hot            heat exchanger effectiveness for hot side                                      efficiency                 :py:meth:`eff_hot_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_hot_func>`
                eff_max            maximum heat exchanger effectiveness                                           efficiency                 :py:meth:`eff_max_func <tespy.components.heat_exchangers.base.HeatExchanger.eff_max_func>`
                UA                 sum of UA values of all sections of heat exchanger                             heat_transfer_coefficient  :py:meth:`UA_func <tespy.components.heat_exchangers.sectioned.SectionedHeatExchanger.UA_func>`
                refrigerant_index  side on which the refrigerant is flowing (0: hot, 1:cold)                      :code:`None`               :code:`None`
                re_exp_r           Reynolds exponent for UA modification based on refrigerant side mass flow      :code:`None`               :code:`None`
                re_exp_sf          Reynolds exponent for UA modification based on secondary fluid side mass flow  :code:`None`               :code:`None`
                alpha_ratio        secondary to refrigerant side convective heat transfer coefficient ratio       ratio                      :code:`None`
                area_ratio         secondary to refrigerant side heat transfer area ratio                         ratio                      :code:`None`
                td_pinch           equation for minimum pinch                                                     temperature_difference     :py:meth:`td_pinch_func <tespy.components.heat_exchangers.sectioned.SectionedHeatExchanger.td_pinch_func>`
                =================  =============================================================================  =========================  ================================================================================================================
                
                Table of parameter groups
                
                =============  ==============================================================  ============================================================================  ====================================================================================================================
                Parameter      Description                                                     Required parameters                                                           Method
                =============  ==============================================================  ============================================================================  ====================================================================================================================
                kA_char        equation for heat transfer based on kA and modification factor  :code:`kA_char1`, :code:`kA_char2`                                            :py:meth:`kA_char_func <tespy.components.heat_exchangers.base.HeatExchanger.kA_char_func>`
                UA_cecchinato  equation for UA modification in offdesign                       :code:`re_exp_r`, :code:`re_exp_sf`, :code:`alpha_ratio`, :code:`area_ratio`  :py:meth:`UA_cecchinato_func <tespy.components.heat_exchangers.sectioned.SectionedHeatExchanger.UA_cecchinato_func>`
                =============  ==============================================================  ============================================================================  ====================================================================================================================
                
                Table of characteristic lines and maps
                
                ===========  ====================================================  ============
                Parameter    Description                                           Method
                ===========  ====================================================  ============
                kA_char1     hot side kA modification lookup table for offdesign   :code:`None`
                kA_char2     cold side kA modification lookup table for offdesign  :code:`None`
                ===========  ====================================================  ============
        
        


            .. dropdown:: SimpleHeatExchanger
                
                Class documentation and example: :py:class:`SimpleHeatExchanger <tespy.components.heat_exchangers.simple.SimpleHeatExchanger>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
                
                Table of parameters
                
                ========================  ==================================================================  =========================  ================================================================================================================
                Parameter                 Description                                                         Quantity                   Method
                ========================  ==================================================================  =========================  ================================================================================================================
                power_connector_location  :code:`None`                                                        :code:`None`               :code:`None`
                Q                         heat transfer                                                       heat                       :py:meth:`energy_balance_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.energy_balance_func>`
                pr                        outlet ot inlet pressure ratio                                      ratio                      :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp                        inlet to outlet absolute pressure change                            pressure                   :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                zeta                      non-dimensional friction coefficient for pressure loss calculation  :code:`None`               :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                D [1]_                    diameter of channel                                                 length                     :code:`None`
                L [1]_                    length of channel                                                   length                     :code:`None`
                ks [1]_                   roughness of wall material                                          length                     :code:`None`
                ks_HW [1]_                Hazen-Williams roughness                                            :code:`None`               :code:`None`
                kA [1]_                   heat transfer coefficient considering ambient temperature           heat_transfer_coefficient  :code:`None`
                Tamb                      ambient temperature                                                 temperature                :code:`None`
                dissipative               :code:`None`                                                        :code:`None`               :code:`None`
                ========================  ==================================================================  =========================  ================================================================================================================
                
                Table of parameter groups
                
                =============  ==================================================================================================  ===================================  ================================================================================================================
                Parameter      Description                                                                                         Required parameters                  Method
                =============  ==================================================================================================  ===================================  ================================================================================================================
                darcy_group    Darcy-Weißbach equation for pressure loss                                                           :code:`L`, :code:`ks`, :code:`D`     :py:meth:`darcy_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.darcy_func>`
                hw_group       Hazen-Williams equation for pressure loss                                                           :code:`L`, :code:`ks_HW`, :code:`D`  :py:meth:`hazen_williams_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.hazen_williams_func>`
                kA_group       equation for heat transfer based on ambient temperature and heat transfer coefficient               :code:`kA`, :code:`Tamb`             :py:meth:`kA_group_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.kA_group_func>`
                kA_char_group  heat transfer from design heat transfer coefficient, modifier lookup table and ambient temperature  :code:`kA_char`, :code:`Tamb`        :py:meth:`kA_char_group_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.kA_char_group_func>`
                =============  ==================================================================================================  ===================================  ================================================================================================================
                
                Table of characteristic lines and maps
                
                ===========  ====================================================  ============
                Parameter    Description                                           Method
                ===========  ====================================================  ============
                kA_char      heat transfer coefficient lookup table for offdesign  :code:`None`
                ===========  ====================================================  ============
        
        


            .. dropdown:: ParabolicTrough
                
                Class documentation and example: :py:class:`ParabolicTrough <tespy.components.heat_exchangers.parabolic_trough.ParabolicTrough>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
                
                Table of parameters
                
                ========================  ==================================================================  ============  ================================================================================================================
                Parameter                 Description                                                         Quantity      Method
                ========================  ==================================================================  ============  ================================================================================================================
                power_connector_location  :code:`None`                                                        :code:`None`  :code:`None`
                Q                         heat transfer                                                       heat          :py:meth:`energy_balance_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.energy_balance_func>`
                pr                        outlet ot inlet pressure ratio                                      ratio         :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp                        inlet to outlet absolute pressure change                            pressure      :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                zeta                      non-dimensional friction coefficient for pressure loss calculation  :code:`None`  :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                D [1]_                    diameter of channel                                                 length        :code:`None`
                L [1]_                    length of channel                                                   length        :code:`None`
                ks [1]_                   roughness of wall material                                          length        :code:`None`
                ks_HW [1]_                Hazen-Williams roughness                                            :code:`None`  :code:`None`
                Tamb                      ambient temperature                                                 temperature   :code:`None`
                dissipative               :code:`None`                                                        :code:`None`  :code:`None`
                E [1]_                    solar irradiation to the parabolic trough                           heat          :code:`None`
                A [1]_                    area of the parabolic trough                                        area          :code:`None`
                eta_opt                   optical efficiency                                                  efficiency    :code:`None`
                c_1                       thermal loss coefficient 1                                          :code:`None`  :code:`None`
                c_2                       thermal loss coefficient 2                                          :code:`None`  :code:`None`
                iam_1                     incidence angle modifier 1                                          :code:`None`  :code:`None`
                iam_2                     incidence angle modifier 2                                          :code:`None`  :code:`None`
                aoi                       angle of incidence                                                  angle         :code:`None`
                doc                       degree of cleanliness                                               ratio         :code:`None`
                Q_loss                    heat dissipation                                                    heat          :code:`None`
                ========================  ==================================================================  ============  ================================================================================================================
                
                Table of parameter groups
                
                ============  ===============================================  =====================================================================================================================================  ==================================================================================================================
                Parameter     Description                                      Required parameters                                                                                                                    Method
                ============  ===============================================  =====================================================================================================================================  ==================================================================================================================
                darcy_group   Darcy-Weißbach equation for pressure loss        :code:`L`, :code:`ks`, :code:`D`                                                                                                       :py:meth:`darcy_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.darcy_func>`
                hw_group      Hazen-Williams equation for pressure loss        :code:`L`, :code:`ks_HW`, :code:`D`                                                                                                    :py:meth:`hazen_williams_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.hazen_williams_func>`
                energy_group  energy balance equation of the parabolic trough  :code:`E`, :code:`eta_opt`, :code:`aoi`, :code:`doc`, :code:`c_1`, :code:`c_2`, :code:`iam_1`, :code:`iam_2`, :code:`A`, :code:`Tamb`  :py:meth:`energy_group_func <tespy.components.heat_exchangers.parabolic_trough.ParabolicTrough.energy_group_func>`
                ============  ===============================================  =====================================================================================================================================  ==================================================================================================================
        
        


            .. dropdown:: ParallelFlowHeatExchanger
                
                Class documentation and example: :py:class:`ParallelFlowHeatExchanger <tespy.components.heat_exchangers.parallel.ParallelFlowHeatExchanger>`
                
                Table of constraints
                
                ==========================  ============================================  =======================================================================================================================
                Parameter                   Description                                   Method
                ==========================  ============================================  =======================================================================================================================
                mass_flow_constraints       mass flow equality constraint(s)              :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints           fluid composition equality constraint(s)      :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                energy_balance_constraints  hot side to cold side heat transfer equation  :py:meth:`energy_balance_func <tespy.components.heat_exchangers.base.HeatExchanger.energy_balance_func>`
                ==========================  ============================================  =======================================================================================================================
                
                Table of parameters
                
                ===========  ============================================================================  =========================  ================================================================================================================
                Parameter    Description                                                                   Quantity                   Method
                ===========  ============================================================================  =========================  ================================================================================================================
                Q            heat transfer from hot side                                                   heat                       :py:meth:`energy_balance_hot_func <tespy.components.heat_exchangers.base.HeatExchanger.energy_balance_hot_func>`
                kA           heat transfer coefficient considering terminal temperature differences        heat_transfer_coefficient  :py:meth:`kA_func <tespy.components.heat_exchangers.base.HeatExchanger.kA_func>`
                td_log       logarithmic temperature difference                                            temperature_difference     :code:`None`
                ttd_u        terminal temperature difference at hot side inlet to cold side outlet         temperature_difference     :py:meth:`ttd_u_func <tespy.components.heat_exchangers.parallel.ParallelFlowHeatExchanger.ttd_u_func>`
                ttd_l        terminal temperature difference at hot side outlet to cold side inlet         temperature_difference     :py:meth:`ttd_l_func <tespy.components.heat_exchangers.parallel.ParallelFlowHeatExchanger.ttd_l_func>`
                pr1          hot side outlet to inlet pressure ratio                                       ratio                      :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                pr2          cold side outlet to inlet pressure ratio                                      ratio                      :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp1          hot side inlet to outlet absolute pressure change                             pressure                   :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                dp2          cold side inlet to outlet absolute pressure change                            pressure                   :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                zeta1        hot side non-dimensional friction coefficient for pressure loss calculation   :code:`None`               :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                zeta2        cold side non-dimensional friction coefficient for pressure loss calculation  :code:`None`               :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                ===========  ============================================================================  =========================  ================================================================================================================
                
                Table of parameter groups
                
                ===========  ==============================================================  ==================================  ==========================================================================================
                Parameter    Description                                                     Required parameters                 Method
                ===========  ==============================================================  ==================================  ==========================================================================================
                kA_char      equation for heat transfer based on kA and modification factor  :code:`kA_char1`, :code:`kA_char2`  :py:meth:`kA_char_func <tespy.components.heat_exchangers.base.HeatExchanger.kA_char_func>`
                ===========  ==============================================================  ==================================  ==========================================================================================
                
                Table of characteristic lines and maps
                
                ===========  ====================================================  ============
                Parameter    Description                                           Method
                ===========  ====================================================  ============
                kA_char1     hot side kA modification lookup table for offdesign   :code:`None`
                kA_char2     cold side kA modification lookup table for offdesign  :code:`None`
                ===========  ====================================================  ============
        
        


            .. dropdown:: SolarCollector
                
                Class documentation and example: :py:class:`SolarCollector <tespy.components.heat_exchangers.solar_collector.SolarCollector>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
                
                Table of parameters
                
                ========================  ==================================================================  ============  ================================================================================================================
                Parameter                 Description                                                         Quantity      Method
                ========================  ==================================================================  ============  ================================================================================================================
                power_connector_location  :code:`None`                                                        :code:`None`  :code:`None`
                Q                         heat transfer                                                       heat          :py:meth:`energy_balance_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.energy_balance_func>`
                pr                        outlet ot inlet pressure ratio                                      ratio         :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp                        inlet to outlet absolute pressure change                            pressure      :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                zeta                      non-dimensional friction coefficient for pressure loss calculation  :code:`None`  :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                D [1]_                    diameter of channel                                                 length        :code:`None`
                L [1]_                    length of channel                                                   length        :code:`None`
                ks [1]_                   roughness of wall material                                          length        :code:`None`
                ks_HW [1]_                Hazen-Williams roughness                                            :code:`None`  :code:`None`
                Tamb                      ambient air temperature                                             temperature   :code:`None`
                dissipative               :code:`None`                                                        :code:`None`  :code:`None`
                E [1]_                    solar irradiation to the solar collector                            heat          :code:`None`
                A [1]_                    area of the solar collector                                         area          :code:`None`
                eta_opt                   optical efficiency                                                  efficiency    :code:`None`
                lkf_lin                   linear heat loss factor                                             :code:`None`  :code:`None`
                lkf_quad                  quadratic heat loss factor                                          :code:`None`  :code:`None`
                Q_loss                    heat dissipation                                                    heat          :code:`None`
                ========================  ==================================================================  ============  ================================================================================================================
                
                Table of parameter groups
                
                ============  ==============================================  ======================================================================================  ================================================================================================================
                Parameter     Description                                     Required parameters                                                                     Method
                ============  ==============================================  ======================================================================================  ================================================================================================================
                darcy_group   Darcy-Weißbach equation for pressure loss       :code:`L`, :code:`ks`, :code:`D`                                                        :py:meth:`darcy_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.darcy_func>`
                hw_group      Hazen-Williams equation for pressure loss       :code:`L`, :code:`ks_HW`, :code:`D`                                                     :py:meth:`hazen_williams_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.hazen_williams_func>`
                energy_group  energy balance equation of the solar collector  :code:`E`, :code:`eta_opt`, :code:`lkf_lin`, :code:`lkf_quad`, :code:`A`, :code:`Tamb`  :py:meth:`energy_group_func <tespy.components.heat_exchangers.solar_collector.SolarCollector.energy_group_func>`
                ============  ==============================================  ======================================================================================  ================================================================================================================
        
        

    .. tab-item:: nodes

        .. container:: accordion-group

            .. dropdown:: NodeBase
                
                Class documentation and example: :py:class:`NodeBase <tespy.components.nodes.base.NodeBase>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
        
        


            .. dropdown:: DropletSeparator
                
                Class documentation and example: :py:class:`DropletSeparator <tespy.components.nodes.droplet_separator.DropletSeparator>`
                
                Table of constraints
                
                ==========================  =======================================  ====================================================================================================================
                Parameter                   Description                              Method
                ==========================  =======================================  ====================================================================================================================
                mass_flow_constraints       mass balance constraint                  :py:meth:`mass_flow_func <tespy.components.nodes.base.NodeBase.mass_flow_func>`
                energy_balance_constraints  energy balance constraint                :py:meth:`energy_balance_func <tespy.components.nodes.droplet_separator.DropletSeparator.energy_balance_func>`
                pressure_constraints        pressure equality constraints            :py:meth:`pressure_structure_matrix <tespy.components.nodes.base.NodeBase.pressure_structure_matrix>`
                outlet_constraint_liquid    outlet 0 is saturated liquid constraint  :py:meth:`saturated_outlet_func <tespy.components.nodes.droplet_separator.DropletSeparator.saturated_outlet_func>`
                outlet_constraint_gas       outlet 1 is saturated liquid constraint  :py:meth:`saturated_outlet_func <tespy.components.nodes.droplet_separator.DropletSeparator.saturated_outlet_func>`
                fluid_constraints           fluid equality constraints               :py:meth:`fluid_structure_matrix <tespy.components.nodes.droplet_separator.DropletSeparator.fluid_structure_matrix>`
                ==========================  =======================================  ====================================================================================================================
        
        


            .. dropdown:: Drum
                
                Class documentation and example: :py:class:`Drum <tespy.components.nodes.drum.Drum>`
                
                Table of constraints
                
                ==========================  =======================================  ====================================================================================================================
                Parameter                   Description                              Method
                ==========================  =======================================  ====================================================================================================================
                mass_flow_constraints       mass balance constraint                  :py:meth:`mass_flow_func <tespy.components.nodes.base.NodeBase.mass_flow_func>`
                energy_balance_constraints  energy balance constraint                :py:meth:`energy_balance_func <tespy.components.nodes.droplet_separator.DropletSeparator.energy_balance_func>`
                pressure_constraints        pressure equality constraints            :py:meth:`pressure_structure_matrix <tespy.components.nodes.base.NodeBase.pressure_structure_matrix>`
                outlet_constraint_liquid    outlet 0 is saturated liquid constraint  :py:meth:`saturated_outlet_func <tespy.components.nodes.droplet_separator.DropletSeparator.saturated_outlet_func>`
                outlet_constraint_gas       outlet 1 is saturated liquid constraint  :py:meth:`saturated_outlet_func <tespy.components.nodes.droplet_separator.DropletSeparator.saturated_outlet_func>`
                fluid_constraints           fluid equality constraints               :py:meth:`fluid_structure_matrix <tespy.components.nodes.droplet_separator.DropletSeparator.fluid_structure_matrix>`
                ==========================  =======================================  ====================================================================================================================
        
        


            .. dropdown:: Merge
                
                Class documentation and example: :py:class:`Merge <tespy.components.nodes.merge.Merge>`
                
                Table of constraints
                
                ==========================  =======================================  =====================================================================================================
                Parameter                   Description                              Method
                ==========================  =======================================  =====================================================================================================
                mass_flow_constraints       mass balance constraint                  :py:meth:`mass_flow_func <tespy.components.nodes.base.NodeBase.mass_flow_func>`
                fluid_constraints           fluid mass fraction balance constraints  :py:meth:`fluid_func <tespy.components.nodes.merge.Merge.fluid_func>`
                energy_balance_constraints  energy balance constraint                :py:meth:`energy_balance_func <tespy.components.nodes.merge.Merge.energy_balance_func>`
                pressure_constraints        pressure equality constraints            :py:meth:`pressure_structure_matrix <tespy.components.nodes.base.NodeBase.pressure_structure_matrix>`
                ==========================  =======================================  =====================================================================================================
                
                Table of parameters
                
                ===========  ================  ============  ============
                Parameter    Description       Quantity      Method
                ===========  ================  ============  ============
                num_in       number of inlets  :code:`None`  :code:`None`
                ===========  ================  ============  ============
        
        


            .. dropdown:: Splitter
                
                Class documentation and example: :py:class:`Splitter <tespy.components.nodes.splitter.Splitter>`
                
                Table of constraints
                
                ==========================  ========================================  =========================================================================================================
                Parameter                   Description                               Method
                ==========================  ========================================  =========================================================================================================
                mass_flow_constraints       mass balance constraint                   :py:meth:`mass_flow_func <tespy.components.nodes.base.NodeBase.mass_flow_func>`
                energy_balance_constraints  equal enthalpy at all outlets constraint  :py:meth:`enthalpy_structure_matrix <tespy.components.nodes.splitter.Splitter.enthalpy_structure_matrix>`
                pressure_constraints        pressure equality constraints             :py:meth:`pressure_structure_matrix <tespy.components.nodes.base.NodeBase.pressure_structure_matrix>`
                fluid_constraints           fluid equality constraints                :py:meth:`fluid_structure_matrix <tespy.components.nodes.splitter.Splitter.fluid_structure_matrix>`
                ==========================  ========================================  =========================================================================================================
                
                Table of parameters
                
                ===========  =================  ============  ============
                Parameter    Description        Quantity      Method
                ===========  =================  ============  ============
                num_out      number of outlets  :code:`None`  :code:`None`
                ===========  =================  ============  ============
        
        


            .. dropdown:: Node
                
                Class documentation and example: :py:class:`Node <tespy.components.nodes.node.Node>`
                
                Table of constraints
                
                ===========================  ===========================================  =====================================================================================================
                Parameter                    Description                                  Method
                ===========================  ===========================================  =====================================================================================================
                mass_flow_constraints        mass balance constraint                      :py:meth:`mass_flow_func <tespy.components.nodes.base.NodeBase.mass_flow_func>`
                pressure_constraints         pressure equality constraints                :py:meth:`pressure_structure_matrix <tespy.components.nodes.base.NodeBase.pressure_structure_matrix>`
                outlet_enthalpy_constraints  equal enthalpy at all outlets constraint(s)  :py:meth:`enthalpy_structure_matrix <tespy.components.nodes.node.Node.enthalpy_structure_matrix>`
                outlet_fluid_constraints     equal fluid at all outlets constraint(s)     :py:meth:`fluid_structure_matrix <tespy.components.nodes.node.Node.fluid_structure_matrix>`
                fluid_constraints            fluid mass fraction constraints              :py:meth:`fluid_func <tespy.components.nodes.merge.Merge.fluid_func>`
                energy_balance_constraints   energy balance constraint                    :py:meth:`energy_balance_func <tespy.components.nodes.merge.Merge.energy_balance_func>`
                ===========================  ===========================================  =====================================================================================================
                
                Table of parameters
                
                ===========  =================  ============  ============
                Parameter    Description        Quantity      Method
                ===========  =================  ============  ============
                num_out      number of outlets  :code:`None`  :code:`None`
                num_in       number of inlets   :code:`None`  :code:`None`
                ===========  =================  ============  ============
        
        


            .. dropdown:: Separator
                
                Class documentation and example: :py:class:`Separator <tespy.components.nodes.separator.Separator>`
                
                Table of constraints
                
                ==========================  ============================================  =====================================================================================================
                Parameter                   Description                                   Method
                ==========================  ============================================  =====================================================================================================
                mass_flow_constraints       mass balance constraint                       :py:meth:`mass_flow_func <tespy.components.nodes.base.NodeBase.mass_flow_func>`
                fluid_constraints           fluid mass fraction balance constraints       :py:meth:`fluid_func <tespy.components.nodes.separator.Separator.fluid_func>`
                energy_balance_constraints  equal temperature at all outlets constraints  :py:meth:`energy_balance_func <tespy.components.nodes.separator.Separator.energy_balance_func>`
                pressure_constraints        pressure equality constraints                 :py:meth:`pressure_structure_matrix <tespy.components.nodes.base.NodeBase.pressure_structure_matrix>`
                ==========================  ============================================  =====================================================================================================
                
                Table of parameters
                
                ===========  =================  ============  ============
                Parameter    Description        Quantity      Method
                ===========  =================  ============  ============
                num_out      number of outlets  :code:`None`  :code:`None`
                ===========  =================  ============  ============
        
        

    .. tab-item:: piping

        .. container:: accordion-group

            .. dropdown:: Pipe
                
                Class documentation and example: :py:class:`Pipe <tespy.components.piping.pipe.Pipe>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
                
                Table of parameters
                
                ========================  ==================================================================  =========================  ================================================================================================================
                Parameter                 Description                                                         Quantity                   Method
                ========================  ==================================================================  =========================  ================================================================================================================
                power_connector_location  :code:`None`                                                        :code:`None`               :code:`None`
                Q                         heat transfer                                                       heat                       :py:meth:`energy_balance_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.energy_balance_func>`
                pr                        outlet ot inlet pressure ratio                                      ratio                      :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp                        inlet to outlet absolute pressure change                            pressure                   :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                zeta                      non-dimensional friction coefficient for pressure loss calculation  :code:`None`               :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                D [1]_                    diameter of channel                                                 length                     :code:`None`
                L [1]_                    length of channel                                                   length                     :code:`None`
                ks [1]_                   roughness of wall material                                          length                     :code:`None`
                ks_HW [1]_                Hazen-Williams roughness                                            :code:`None`               :code:`None`
                kA [1]_                   heat transfer coefficient considering ambient temperature           heat_transfer_coefficient  :code:`None`
                Tamb                      ambient temperature                                                 temperature                :code:`None`
                dissipative               :code:`None`                                                        :code:`None`               :code:`None`
                insulation_thickness      thickness of pipe insulation                                        length                     :code:`None`
                insulation_tc             thermal conductivity of insulation                                  thermal_conductivity       :code:`None`
                material                  :code:`None`                                                        :code:`None`               :code:`None`
                pipe_thickness            wall thickness of pipe                                              length                     :code:`None`
                environment_media         :code:`None`                                                        :code:`None`               :code:`None`
                wind_velocity             velocity of wind at insulation surface                              speed                      :code:`None`
                pipe_depth                depth of buried pipe                                                length                     :code:`None`
                ========================  ==================================================================  =========================  ================================================================================================================
                
                Table of parameter groups
                
                ======================  ==================================================================================================  =============================================================================================================================================================  ================================================================================================================
                Parameter               Description                                                                                         Required parameters                                                                                                                                            Method
                ======================  ==================================================================================================  =============================================================================================================================================================  ================================================================================================================
                darcy_group             Darcy-Weißbach equation for pressure loss                                                           :code:`L`, :code:`ks`, :code:`D`                                                                                                                               :py:meth:`darcy_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.darcy_func>`
                hw_group                Hazen-Williams equation for pressure loss                                                           :code:`L`, :code:`ks_HW`, :code:`D`                                                                                                                            :py:meth:`hazen_williams_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.hazen_williams_func>`
                kA_group                equation for heat transfer based on ambient temperature and heat transfer coefficient               :code:`kA`, :code:`Tamb`                                                                                                                                       :py:meth:`kA_group_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.kA_group_func>`
                kA_char_group           heat transfer from design heat transfer coefficient, modifier lookup table and ambient temperature  :code:`kA_char`, :code:`Tamb`                                                                                                                                  :py:meth:`kA_char_group_func <tespy.components.heat_exchangers.simple.SimpleHeatExchanger.kA_char_group_func>`
                Q_ohc_group_surface     equation for heat loss of surface pipes                                                             :code:`insulation_thickness`, :code:`insulation_tc`, :code:`Tamb`, :code:`material`, :code:`pipe_thickness`, :code:`environment_media`, :code:`wind_velocity`  :py:meth:`ohc_surface_group_func <tespy.components.piping.pipe.Pipe.ohc_surface_group_func>`
                Q_ohc_group_subsurface  equation for heat loss of buried pipes                                                              :code:`insulation_thickness`, :code:`insulation_tc`, :code:`Tamb`, :code:`material`, :code:`pipe_thickness`, :code:`environment_media`, :code:`pipe_depth`     :py:meth:`ohc_subsurface_group_func <tespy.components.piping.pipe.Pipe.ohc_subsurface_group_func>`
                ======================  ==================================================================================================  =============================================================================================================================================================  ================================================================================================================
                
                Table of characteristic lines and maps
                
                ===========  ====================================================  ============
                Parameter    Description                                           Method
                ===========  ====================================================  ============
                kA_char      heat transfer coefficient lookup table for offdesign  :code:`None`
                ===========  ====================================================  ============
        
        


            .. dropdown:: Valve
                
                Class documentation and example: :py:class:`Valve <tespy.components.piping.valve.Valve>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                enthalpy_constraints   equation for enthalpy equality            :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
                
                Table of parameters
                
                ===========  ========================================  ============  =========================================================================================
                Parameter    Description                               Quantity      Method
                ===========  ========================================  ============  =========================================================================================
                pr           :code:`None`                              ratio         :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp           inlet to outlet absolute pressure change  pressure      :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                zeta         :code:`None`                              :code:`None`  :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                ===========  ========================================  ============  =========================================================================================
                
                Table of characteristic lines and maps
                
                ===========  ==============================================================================  ==========================================================================
                Parameter    Description                                                                     Method
                ===========  ==============================================================================  ==========================================================================
                dp_char      inlet to outlet absolute pressure change as function of mass flow lookup table  :py:meth:`dp_char_func <tespy.components.piping.valve.Valve.dp_char_func>`
                ===========  ==============================================================================  ==========================================================================
        
        

    .. tab-item:: power

        .. container:: accordion-group

            .. dropdown:: PowerBus
                
                Class documentation and example: :py:class:`PowerBus <tespy.components.power.bus.PowerBus>`
                
                Table of constraints
                
                =========================  ============================================  ========================================================================================
                Parameter                  Description                                   Method
                =========================  ============================================  ========================================================================================
                energy_balance_constraint  energy balance over all inflows and outflows  :py:meth:`energy_balance_func <tespy.components.power.bus.PowerBus.energy_balance_func>`
                =========================  ============================================  ========================================================================================
                
                Table of parameters
                
                ===========  =================  ============  ============
                Parameter    Description        Quantity      Method
                ===========  =================  ============  ============
                num_in       number of inlets   :code:`None`  :code:`None`
                num_out      number of outlets  :code:`None`  :code:`None`
                ===========  =================  ============  ============
        
        


            .. dropdown:: Generator
                
                Class documentation and example: :py:class:`Generator <tespy.components.power.generator.Generator>`
                
                Table of parameters
                
                ===========  ================================  ==========  =========================================================================================
                Parameter    Description                       Quantity    Method
                ===========  ================================  ==========  =========================================================================================
                eta          efficiency                        efficiency  :py:meth:`eta_func <tespy.components.power.generator.Generator.eta_func>`
                delta_power  inlet to outlet power difference  power       :py:meth:`delta_power_func <tespy.components.power.generator.Generator.delta_power_func>`
                ===========  ================================  ==========  =========================================================================================
                
                Table of characteristic lines and maps
                
                ===========  =====================================  ===================================================================================
                Parameter    Description                            Method
                ===========  =====================================  ===================================================================================
                eta_char     efficiency lookup table for offdesign  :py:meth:`eta_char_func <tespy.components.power.generator.Generator.eta_char_func>`
                ===========  =====================================  ===================================================================================
        
        


            .. dropdown:: Motor
                
                Class documentation and example: :py:class:`Motor <tespy.components.power.motor.Motor>`
                
                Table of parameters
                
                ===========  ================================  ==========  =================================================================================
                Parameter    Description                       Quantity    Method
                ===========  ================================  ==========  =================================================================================
                eta          efficiency                        efficiency  :py:meth:`eta_func <tespy.components.power.motor.Motor.eta_func>`
                delta_power  inlet to outlet power difference  power       :py:meth:`delta_power_func <tespy.components.power.motor.Motor.delta_power_func>`
                ===========  ================================  ==========  =================================================================================
                
                Table of characteristic lines and maps
                
                ===========  =====================================  ===========================================================================
                Parameter    Description                            Method
                ===========  =====================================  ===========================================================================
                eta_char     efficiency lookup table for offdesign  :py:meth:`eta_char_func <tespy.components.power.motor.Motor.eta_char_func>`
                ===========  =====================================  ===========================================================================
        
        


            .. dropdown:: PowerSink
                
                Class documentation and example: :py:class:`PowerSink <tespy.components.power.sink.PowerSink>`
        
        


            .. dropdown:: PowerSource
                
                Class documentation and example: :py:class:`PowerSource <tespy.components.power.source.PowerSource>`
        
        

    .. tab-item:: reactors

        .. container:: accordion-group

            .. dropdown:: FuelCell
                
                Class documentation and example: :py:class:`FuelCell <tespy.components.reactors.fuel_cell.FuelCell>`
                
                Table of constraints
                
                =============================  ====================================================  ===============================================================================================================================
                Parameter                      Description                                           Method
                =============================  ====================================================  ===============================================================================================================================
                mass_flow_constraints          equations for oxygen and hydrogen mass flow relation  :py:meth:`reactor_mass_flow_func <tespy.components.reactors.fuel_cell.FuelCell.reactor_mass_flow_func>`
                cooling_mass_flow_constraints  cooling fluid mass flow equality equation             :py:meth:`cooling_mass_flow_structure_matrix <tespy.components.reactors.fuel_cell.FuelCell.cooling_mass_flow_structure_matrix>`
                cooling_fluid_constraints      cooling fluid composition equality equation           :py:meth:`cooling_fluid_structure_matrix <tespy.components.reactors.fuel_cell.FuelCell.cooling_fluid_structure_matrix>`
                energy_balance_constraints     energy balance equation of the reactor                :py:meth:`energy_balance_func <tespy.components.reactors.fuel_cell.FuelCell.energy_balance_func>`
                reactor_pressure_constraints   reactor pressure equality equations                   :py:meth:`reactor_pressure_structure_matrix <tespy.components.reactors.fuel_cell.FuelCell.reactor_pressure_structure_matrix>`
                =============================  ====================================================  ===============================================================================================================================
                
                Table of parameters
                
                ===========  ===============================================================================  ===============  ===================================================================================================
                Parameter    Description                                                                      Quantity         Method
                ===========  ===============================================================================  ===============  ===================================================================================================
                P [1]_       power output of the fuel cell                                                    power            :code:`None`
                Q            heat output of the cooling port                                                  heat             :py:meth:`heat_func <tespy.components.reactors.fuel_cell.FuelCell.heat_func>`
                pr           cooling port outlet to inlet pressure ratio                                      ratio            :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp           cooling inlet to outlet absolute pressure change                                 pressure         :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                zeta         cooling port non-dimensional friction coefficient for pressure loss calculation  :code:`None`     :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                eta          efficiency of the fuel cell                                                      efficiency       :py:meth:`eta_func <tespy.components.reactors.fuel_cell.FuelCell.eta_func>`
                e [1]_       equation for specified specific energy consumption of the fuel cell              specific_energy  :py:meth:`specific_energy_func <tespy.components.reactors.fuel_cell.FuelCell.specific_energy_func>`
                ===========  ===============================================================================  ===============  ===================================================================================================
        
        


            .. dropdown:: WaterElectrolyzer
                
                Class documentation and example: :py:class:`WaterElectrolyzer <tespy.components.reactors.water_electrolyzer.WaterElectrolyzer>`
                
                Table of constraints
                
                =============================  ====================================================  =================================================================================================================================================
                Parameter                      Description                                           Method
                =============================  ====================================================  =================================================================================================================================================
                mass_flow_constraints          equations for oxygen and hydrogen mass flow relation  :py:meth:`reactor_mass_flow_func <tespy.components.reactors.water_electrolyzer.WaterElectrolyzer.reactor_mass_flow_func>`
                cooling_mass_flow_constraints  cooling fluid mass flow equality equation             :py:meth:`cooling_mass_flow_structure_matrix <tespy.components.reactors.water_electrolyzer.WaterElectrolyzer.cooling_mass_flow_structure_matrix>`
                cooling_fluid_constraints      cooling fluid composition equality equation           :py:meth:`cooling_fluid_structure_matrix <tespy.components.reactors.water_electrolyzer.WaterElectrolyzer.cooling_fluid_structure_matrix>`
                energy_balance_constraints     energy balance equation of the reactor                :py:meth:`energy_balance_func <tespy.components.reactors.water_electrolyzer.WaterElectrolyzer.energy_balance_func>`
                reactor_pressure_constraints   reactor pressure equality equations                   :py:meth:`reactor_pressure_structure_matrix <tespy.components.reactors.water_electrolyzer.WaterElectrolyzer.reactor_pressure_structure_matrix>`
                gas_temperature_constraints    equation for same temperature of product gases        :py:meth:`gas_temperature_func <tespy.components.reactors.water_electrolyzer.WaterElectrolyzer.gas_temperature_func>`
                =============================  ====================================================  =================================================================================================================================================
                
                Table of parameters
                
                ===========  ===============================================================================  ===============  =====================================================================================================================
                Parameter    Description                                                                      Quantity         Method
                ===========  ===============================================================================  ===============  =====================================================================================================================
                P [1]_       power consumption of the electrolyzer                                            power            :code:`None`
                Q            heat output of the cooling port                                                  heat             :py:meth:`heat_func <tespy.components.reactors.water_electrolyzer.WaterElectrolyzer.heat_func>`
                pr           cooling port outlet to inlet pressure ratio                                      ratio            :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp           cooling inlet to outlet absolute pressure change                                 pressure         :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                zeta         cooling port non-dimensional friction coefficient for pressure loss calculation  :code:`None`     :py:meth:`zeta_func <tespy.components.component.Component.zeta_func>`
                eta          efficiency of the fuel cell                                                      efficiency       :py:meth:`eta_func <tespy.components.reactors.water_electrolyzer.WaterElectrolyzer.eta_func>`
                e [1]_       equation for specified specific energy consumption of the electrolyzer           specific_energy  :py:meth:`specific_energy_func <tespy.components.reactors.water_electrolyzer.WaterElectrolyzer.specific_energy_func>`
                ===========  ===============================================================================  ===============  =====================================================================================================================
                
                Table of characteristic lines and maps
                
                ===========  =====================================  =======================================================================================================
                Parameter    Description                            Method
                ===========  =====================================  =======================================================================================================
                eta_char     efficiency lookup table for offdesign  :py:meth:`eta_char_func <tespy.components.reactors.water_electrolyzer.WaterElectrolyzer.eta_char_func>`
                ===========  =====================================  =======================================================================================================
        
        

    .. tab-item:: turbomachinery

        .. container:: accordion-group

            .. dropdown:: Turbomachine
                
                Class documentation and example: :py:class:`Turbomachine <tespy.components.turbomachinery.base.Turbomachine>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
                
                Table of parameters
                
                ===========  ========================================  ==========  ======================================================================================================
                Parameter    Description                               Quantity    Method
                ===========  ========================================  ==========  ======================================================================================================
                P            power input/output of the component       power       :py:meth:`energy_balance_func <tespy.components.turbomachinery.base.Turbomachine.energy_balance_func>`
                pr           outlet to inlet pressure ratio            ratio       :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp           inlet to outlet absolute pressure change  pressure    :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                ===========  ========================================  ==========  ======================================================================================================
        
        


            .. dropdown:: Compressor
                
                Class documentation and example: :py:class:`Compressor <tespy.components.turbomachinery.compressor.Compressor>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
                
                Table of parameters
                
                ===========  ========================================  ==========  ======================================================================================================
                Parameter    Description                               Quantity    Method
                ===========  ========================================  ==========  ======================================================================================================
                P            power input/output of the component       power       :py:meth:`energy_balance_func <tespy.components.turbomachinery.base.Turbomachine.energy_balance_func>`
                pr           outlet to inlet pressure ratio            ratio       :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp           inlet to outlet absolute pressure change  pressure    :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                eta_s        isentropic efficiency                     efficiency  :py:meth:`eta_s_func <tespy.components.turbomachinery.compressor.Compressor.eta_s_func>`
                igva [1]_    inlet guide vane angle                    angle       :code:`None`
                ===========  ========================================  ==========  ======================================================================================================
                
                Table of parameter groups
                
                ====================  ===========================================================================  ====================================  ==========================================================================================================
                Parameter             Description                                                                  Required parameters                   Method
                ====================  ===========================================================================  ====================================  ==========================================================================================================
                char_map_eta_s_group  map for isentropic efficiency over speedlines and non-dimensional mass flow  :code:`char_map_eta_s`, :code:`igva`  :py:meth:`char_map_eta_s_func <tespy.components.turbomachinery.compressor.Compressor.char_map_eta_s_func>`
                char_map_pr_group     map for pressure ratio over speedlines and non-dimensional mass flow         :code:`char_map_pr`, :code:`igva`     :py:meth:`char_map_pr_func <tespy.components.turbomachinery.compressor.Compressor.char_map_pr_func>`
                ====================  ===========================================================================  ====================================  ==========================================================================================================
                
                Table of characteristic lines and maps
                
                ==============  ================================================================================  ==================================================================================================
                Parameter       Description                                                                       Method
                ==============  ================================================================================  ==================================================================================================
                eta_s_char      isentropic efficiency lookup table for offdesign                                  :py:meth:`eta_s_char_func <tespy.components.turbomachinery.compressor.Compressor.eta_s_char_func>`
                char_map_eta_s  2D lookup table for efficiency over non-dimensional mass flow and speed line      :code:`None`
                char_map_pr     2D lookup table for pressure ratio over non-dimensional mass flow and speed line  :code:`None`
                ==============  ================================================================================  ==================================================================================================
        
        


            .. dropdown:: Pump
                
                Class documentation and example: :py:class:`Pump <tespy.components.turbomachinery.pump.Pump>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
                
                Table of parameters
                
                ===========  ========================================  ==========  ======================================================================================================
                Parameter    Description                               Quantity    Method
                ===========  ========================================  ==========  ======================================================================================================
                P            power input/output of the component       power       :py:meth:`energy_balance_func <tespy.components.turbomachinery.base.Turbomachine.energy_balance_func>`
                pr           outlet to inlet pressure ratio            ratio       :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp           inlet to outlet absolute pressure change  pressure    :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                eta_s        isentropic efficiency                     efficiency  :py:meth:`eta_s_func <tespy.components.turbomachinery.pump.Pump.eta_s_func>`
                ===========  ========================================  ==========  ======================================================================================================
                
                Table of characteristic lines and maps
                
                ===========  ================================================  ======================================================================================
                Parameter    Description                                       Method
                ===========  ================================================  ======================================================================================
                eta_s_char   isentropic efficiency lookup table for offdesign  :py:meth:`eta_s_char_func <tespy.components.turbomachinery.pump.Pump.eta_s_char_func>`
                flow_char    pressure rise over volumetric flow lookup table   :py:meth:`flow_char_func <tespy.components.turbomachinery.pump.Pump.flow_char_func>`
                ===========  ================================================  ======================================================================================
        
        


            .. dropdown:: Turbine
                
                Class documentation and example: :py:class:`Turbine <tespy.components.turbomachinery.turbine.Turbine>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
                
                Table of parameters
                
                ===========  ========================================  ============  ======================================================================================================
                Parameter    Description                               Quantity      Method
                ===========  ========================================  ============  ======================================================================================================
                P            power input/output of the component       power         :py:meth:`energy_balance_func <tespy.components.turbomachinery.base.Turbomachine.energy_balance_func>`
                pr           outlet to inlet pressure ratio            ratio         :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp           inlet to outlet absolute pressure change  pressure      :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                eta_s        isentropic efficiency                     efficiency    :py:meth:`eta_s_func <tespy.components.turbomachinery.turbine.Turbine.eta_s_func>`
                cone         cone law equation for offdesign           :code:`None`  :py:meth:`cone_func <tespy.components.turbomachinery.turbine.Turbine.cone_func>`
                ===========  ========================================  ============  ======================================================================================================
                
                Table of characteristic lines and maps
                
                ===========  ================================================  ============================================================================================
                Parameter    Description                                       Method
                ===========  ================================================  ============================================================================================
                eta_s_char   isentropic efficiency lookup table for offdesign  :py:meth:`eta_s_char_func <tespy.components.turbomachinery.turbine.Turbine.eta_s_char_func>`
                ===========  ================================================  ============================================================================================
        
        


            .. dropdown:: SteamTurbine
                
                Class documentation and example: :py:class:`SteamTurbine <tespy.components.turbomachinery.steam_turbine.SteamTurbine>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
                
                Table of parameters
                
                ===========  ================================================  ============  ======================================================================================================
                Parameter    Description                                       Quantity      Method
                ===========  ================================================  ============  ======================================================================================================
                P            power input/output of the component               power         :py:meth:`energy_balance_func <tespy.components.turbomachinery.base.Turbomachine.energy_balance_func>`
                pr           outlet to inlet pressure ratio                    ratio         :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp           inlet to outlet absolute pressure change          pressure      :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                eta_s        isentropic efficiency                             efficiency    :py:meth:`eta_s_func <tespy.components.turbomachinery.turbine.Turbine.eta_s_func>`
                cone         cone law equation for offdesign                   :code:`None`  :py:meth:`cone_func <tespy.components.turbomachinery.turbine.Turbine.cone_func>`
                alpha        influence factor for wetness efficiency modifier  ratio         :code:`None`
                eta_s_dry    isentropic efficiency of dry expansion            efficiency    :code:`None`
                ===========  ================================================  ============  ======================================================================================================
                
                Table of parameter groups
                
                ===============  ============================  ================================  =====================================================================================================
                Parameter        Description                   Required parameters               Method
                ===============  ============================  ================================  =====================================================================================================
                eta_s_dry_group  method to apply Baumann rule  :code:`alpha`, :code:`eta_s_dry`  :py:meth:`eta_s_wet_func <tespy.components.turbomachinery.steam_turbine.SteamTurbine.eta_s_wet_func>`
                ===============  ============================  ================================  =====================================================================================================
                
                Table of characteristic lines and maps
                
                ===========  ================================================  ============================================================================================
                Parameter    Description                                       Method
                ===========  ================================================  ============================================================================================
                eta_s_char   isentropic efficiency lookup table for offdesign  :py:meth:`eta_s_char_func <tespy.components.turbomachinery.turbine.Turbine.eta_s_char_func>`
                ===========  ================================================  ============================================================================================
        
        


            .. dropdown:: TurboCompressor
                
                Class documentation and example: :py:class:`TurboCompressor <tespy.components.turbomachinery.turbocompressor.TurboCompressor>`
                
                Table of constraints
                
                =====================  ========================================  =======================================================================================================================
                Parameter              Description                               Method
                =====================  ========================================  =======================================================================================================================
                mass_flow_constraints  mass flow equality constraint(s)          :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                fluid_constraints      fluid composition equality constraint(s)  :py:meth:`variable_equality_structure_matrix <tespy.components.component.Component.variable_equality_structure_matrix>`
                =====================  ========================================  =======================================================================================================================
                
                Table of parameters
                
                ===========  ========================================  ==========  ======================================================================================================
                Parameter    Description                               Quantity    Method
                ===========  ========================================  ==========  ======================================================================================================
                P            power input/output of the component       power       :py:meth:`energy_balance_func <tespy.components.turbomachinery.base.Turbomachine.energy_balance_func>`
                pr           outlet to inlet pressure ratio            ratio       :py:meth:`pr_structure_matrix <tespy.components.component.Component.pr_structure_matrix>`
                dp           inlet to outlet absolute pressure change  pressure    :py:meth:`dp_structure_matrix <tespy.components.component.Component.dp_structure_matrix>`
                eta_s        isentropic efficiency                     efficiency  :py:meth:`eta_s_func <tespy.components.turbomachinery.compressor.Compressor.eta_s_func>`
                igva [1]_    inlet guide vane angle                    angle       :code:`None`
                ===========  ========================================  ==========  ======================================================================================================
                
                Table of parameter groups
                
                ====================  ===========================================================================  ====================================  ====================================================================================================================
                Parameter             Description                                                                  Required parameters                   Method
                ====================  ===========================================================================  ====================================  ====================================================================================================================
                char_map_eta_s_group  map for isentropic efficiency over speedlines and non-dimensional mass flow  :code:`char_map_eta_s`, :code:`igva`  :py:meth:`char_map_eta_s_func <tespy.components.turbomachinery.turbocompressor.TurboCompressor.char_map_eta_s_func>`
                char_map_pr_group     map for pressure ratio over speedlines and non-dimensional mass flow         :code:`char_map_pr`, :code:`igva`     :py:meth:`char_map_pr_func <tespy.components.turbomachinery.turbocompressor.TurboCompressor.char_map_pr_func>`
                ====================  ===========================================================================  ====================================  ====================================================================================================================
                
                Table of characteristic lines and maps
                
                ==============  ================================================================================  ============
                Parameter       Description                                                                       Method
                ==============  ================================================================================  ============
                char_map_eta_s  2D lookup table for efficiency over non-dimensional mass flow and speed line      :code:`None`
                char_map_pr     2D lookup table for pressure ratio over non-dimensional mass flow and speed line  :code:`None`
                ==============  ================================================================================  ============
        
        

.. [1] This parameter can be made a variable, :ref:`get more info here <component_variables_label>`.