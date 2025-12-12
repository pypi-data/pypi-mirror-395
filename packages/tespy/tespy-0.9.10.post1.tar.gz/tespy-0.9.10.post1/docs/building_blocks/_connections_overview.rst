.. tab-set::

    .. tab-item:: Connection

        Class documentation and example: :py:class:`Connection <tespy.connections.connection.Connection>`
        
        Table of parameters
        
        =============  ===============================================================================================  ======================  ==============================================================================================================
        Parameter      Description                                                                                      Quantity                Method
        =============  ===============================================================================================  ======================  ==============================================================================================================
        m              mass flow of the fluid (system variable)                                                         mass_flow               :code:`None`
        p              absolute pressure of the fluid (system variable)                                                 pressure                :code:`None`
        h              mass specific enthalpy of the fluid (system variable)                                            enthalpy                :code:`None`
        T              temperature of the fluid                                                                         temperature             :py:meth:`T_func <tespy.connections.connection.Connection.T_func>`
        T_bubble       determine pressure based on the provided bubble temperature of the fluid                         temperature             :code:`None`
        T_dew          determine pressure based on the provided dew temperature of the fluid                            temperature             :code:`None`
        v              volumetric flow of the fluid                                                                     volumetric_flow         :py:meth:`v_func <tespy.connections.connection.Connection.v_func>`
        x              vapor mass fraction/quality of the two-phase fluid                                               quality                 :py:meth:`x_func <tespy.connections.connection.Connection.x_func>`
        td_dew         superheating temperature difference to dew line temperature                                      temperature_difference  :py:meth:`td_dew_func <tespy.connections.connection.Connection.td_dew_func>`
        td_bubble      subcooling temperature difference to bubble line temperature                                     temperature_difference  :py:meth:`td_bubble_func <tespy.connections.connection.Connection.td_bubble_func>`
        m_ref          equation for linear relationship between two mass flows                                          mass_flow               :py:meth:`primary_ref_structure_matrix <tespy.connections.connection.Connection.primary_ref_structure_matrix>`
        p_ref          equation for linear relationship between two pressure values                                     pressure                :py:meth:`primary_ref_structure_matrix <tespy.connections.connection.Connection.primary_ref_structure_matrix>`
        h_ref          equation for linear relationship between two enthalpy values                                     enthalpy                :py:meth:`primary_ref_structure_matrix <tespy.connections.connection.Connection.primary_ref_structure_matrix>`
        T_ref          equation for linear relationship between two temperature values                                  temperature_difference  :py:meth:`T_ref_func <tespy.connections.connection.Connection.T_ref_func>`
        v_ref          equation for linear relationship between two volumetric flows                                    volumetric_flow         :py:meth:`v_ref_func <tespy.connections.connection.Connection.v_ref_func>`
        vol            specific volume of the fluid (output only)                                                       specific_volume         :code:`None`
        s              specific entropy of the fluid (output only)                                                      entropy                 :code:`None`
        fluid          mass fractions of the fluid composition (system variable)                                        :code:`None`            :code:`None`
        fluid_balance  apply an equation which closes the fluid balance with at least two unknown fluid mass fractions  :code:`None`            :py:meth:`fluid_balance_func <tespy.connections.connection.Connection.fluid_balance_func>`
        Td_bp          temperature difference to boiling point (deprecated)                                             temperature_difference  :py:meth:`Td_bp_func <tespy.connections.connection.Connection.Td_bp_func>`
        =============  ===============================================================================================  ======================  ==============================================================================================================
        
        

    .. tab-item:: PowerConnection

        Class documentation and example: :py:class:`PowerConnection <tespy.connections.powerconnection.PowerConnection>`
        
        Table of parameters
        
        ===========  =============  ==========  ============
        Parameter    Description    Quantity    Method
        ===========  =============  ==========  ============
        E            :code:`None`   power       :code:`None`
        ===========  =============  ==========  ============
        
        

