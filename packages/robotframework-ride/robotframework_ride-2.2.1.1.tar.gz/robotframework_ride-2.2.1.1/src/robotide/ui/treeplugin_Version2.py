class Tree(treemixin.DragAndDrop, customtreectrl.CustomTreeCtrl, wx.Panel):
    def __init__(self, parent, action_registerer, settings=None):
        ...
        self._rendered_resources = set()  # <-- Add this line to track rendered resources
        ...

    def _clear_tree_data(self):
        self.DeleteAllItems()
        self.root = self.AddRoot('')
        self._resource_root = self._create_resource_root()
        self.datafile_nodes = []
        self._resources = []
        self.controller.clear_history()
        self._rendered_resources = set()  # <-- Reset on tree clear

    def _populate_model(self, model):
        handler = ResourceRootHandler(model, self, self._resource_root,
                                      self.controller.settings)
        self.SetPyData(self._resource_root, handler)
        if model.data:
            self._render_datafile(self.root, model.data, 0)
        for res in model.external_resources:
            if not res.parent and res not in self._rendered_resources:
                self._render_datafile(self._resource_root, res)
                self._rendered_resources.add(res)  # <-- Mark as rendered

    def _resource_added(self, message):
        ctrl = message.datafile
        if self.controller.find_node_by_controller(ctrl):
            return
        # Prevent duplicate resource nodes
        if ctrl in self._rendered_resources:
            return
        if ctrl.parent:
            parent = self._get_dir_node(ctrl.parent)
        else:
            parent = self._resource_root
        self._render_datafile(parent, ctrl)
        self._rendered_resources.add(ctrl)  # <-- Mark as rendered