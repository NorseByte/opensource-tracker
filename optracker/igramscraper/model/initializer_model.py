import time


class InitializerModel:

    def __init__(self, props=None):

        self._is_new = True
        self._is_loaded = False
        """init data was empty"""
        self._is_load_empty = True
        self._is_fake = False
        self._modified = None

        """Array of initialization data"""
        self._data = {}

        self.modified = time.time()

        if props is not None and len(props) > 0:
            self._init(props)

    def _init(self, props):
        """

        :param props: props array
        :return: None
        """
        for key in props.keys():
            try:
                self._init_properties_custom(props[key], key, props)
            except AttributeError:
                # if function does not exist fill help data array
                self._data[key] = props[key]

        self._is_new = False
        self._is_loaded = True
        self._is_load_empty = False

    # '''
    #  * @return $this
    #  '''
    # @staticmethod
    # def fake():
    #     return static::create()->setFake(true);

    # '''
    #  * @param bool $value
    #  *
    #  * @return $this
    #  '''
    # def _setFake(self, value = True):
    #     self._isFake = (bool)value

    # '''
    #  * @return bool
    #  '''
    # public function isNotEmpty()
    # {
    #     return !$this->isLoadEmpty;
    # }

    # '''
    #  * @return bool
    #  '''
    # public function isFake()
    # {
    #     return $this->isFake;
    # }

    # '''
    #  * @return array
    #  '''
    # public function toArray()
    # {
    #     ret = []
    #     map = static::$initPropertiesMap;
    #     foreach ($map as $key => $init) {
    #         if (\property_exists($this, $key)) {
    #             //if there is property then it just assign value
    #             $ret[$key] = $this->{$key};
    #         } elseif (isset($this[$key])) {
    #             //probably array access
    #             $ret[$key] = $this[$key];
    #         } else {
    #             $ret[$key] = null;
    #         }
    #     }

    #     return $ret;
    # }

    # '''
    #  * @param $datetime
    #  *
    #  * @return $this
    #  '''
    # protected function initModified($datetime)
    # {
    #     $this->modified = \strtotime($datetime);

    #     return $this;
    # }

    # '''
    #  * @param string $date
    #  * @param string $key
    #  *
    #  * @return $this
    #  '''
    # protected function initDatetime($date, $key)
    # {
    #     return $this->initProperty(\strtotime($date), $key);
    # }

    # '''
    #  * @param $value
    #  * @param $key
    #  *
    #  * @return $this
    #  '''
    # protected function initProperty($value, $key)
    # {
    #     $keys = \func_get_args();
    #     unset($keys[0]); //remove value
    #     if (\count($keys) > 1) {
    #         foreach ($keys as $key) {
    #             if (\property_exists($this, $key)) { //first found set
    #                 $this->{$key} = $value;

    #                 return $this;
    #             }
    #         }
    #     } elseif (\property_exists($this, $key)) {
    #         $this->{$key} = $value;
    #     }

    #     return $this;
    # }

    # '''
    #  * @param mixed $value
    #  * @param string $key
    #  *
    #  * @return $this
    #  '''
    # protected function initBool($value, $key)
    # {
    #     return $this->initProperty(!empty($value), "is{$key}", $key);
    # }

    # '''
    #  * @param mixed $value
    #  * @param string $key
    #  *
    #  * @return $this
    #  '''
    # protected function initInt($value, $key)
    # {
    #     return $this->initProperty((int)$value, $key);
    # }

    # '''
    #  * @param mixed $value
    #  * @param string $key
    #  *
    #  * @return $this
    #  '''
    # protected function initFloat($value, $key)
    # {
    #     return $this->initProperty((float)$value, $key);
    # }

    # '''
    #  * @param string $rawData
    #  * @param string $key
    #  *
    #  * @return $this
    #  '''
    # def _initJsonArray(rawData, key):

    #     value = json.loads(rawData)
    #     if value == None or len(value) == 0:
    #         if ('null' == rawData or '' == rawData or 'None' == rawData):
    #             value = []
    #         else:
    #             value = (array)rawData;
    #     else
    #         value = (array)$value;

    #     return $this->initProperty($value, $key);

    # '''
    #  * @param mixed $value
    #  * @param string $key
    #  *
    #  * @return $this
    #  '''
    # protected function initExplode($value, $key)
    # {
    #     return $this->initProperty(\explode(',', $value), "is{$key}", $key);
    # }
